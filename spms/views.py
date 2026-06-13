from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.http import HttpResponseForbidden
from .models import User, Achievement, PointRule
from .forms import RegisterForm, LoginForm, AchievementForm, ReviewForm


# ─────────────────────────────────────────────
# AUTH VIEWS
# ─────────────────────────────────────────────

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    point_rules = PointRule.objects.all()
    return render(request, 'spms/index.html', {'point_rules': point_rules})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    return render(request, 'spms/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        # Allow login by enrollment_no too
        username_input = request.POST.get('username', '')
        password_input = request.POST.get('password', '')

        # Try enrollment_no lookup
        user_obj = None
        try:
            u = User.objects.get(enrollment_no=username_input)
            user_obj = authenticate(request, username=u.username, password=password_input)
        except User.DoesNotExist:
            user_obj = authenticate(request, username=username_input, password=password_input)

        if user_obj:
            login(request, user_obj)
            messages.success(request, f'Welcome back, {user_obj.first_name or user_obj.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'spms/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─────────────────────────────────────────────
# ROLE ROUTER
# ─────────────────────────────────────────────

@login_required
def dashboard(request):
    role = request.user.role
    if role == 'student':
        return redirect('student_dashboard')
    elif role == 'faculty':
        return redirect('faculty_dashboard')
    elif role == 'admin':
        return redirect('admin_dashboard')
    return redirect('login')


# ─────────────────────────────────────────────
# STUDENT VIEWS
# ─────────────────────────────────────────────

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return HttpResponseForbidden()

    user = request.user
    achievements = user.achievements.all()
    total_score = user.get_total_score()
    score_by_cat = user.get_score_by_category()

    stats = {
        'total': achievements.count(),
        'approved': achievements.filter(status='approved').count(),
        'pending': achievements.filter(status='pending').count(),
        'rejected': achievements.filter(status='rejected').count(),
    }

    # Leaderboard position
    all_students = User.objects.filter(role='student')
    scored = sorted(all_students, key=lambda u: u.get_total_score(), reverse=True)
    rank = next((i+1 for i, u in enumerate(scored) if u.pk == user.pk), '-')

    form = AchievementForm()
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            ach = form.save(commit=False)
            ach.student = user
            ach.auto_assign_points()
            ach.save()
            messages.success(request, f'Achievement submitted! Points will be awarded after faculty review.')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Please fix the errors in the form.')

    context = {
        'user': user,
        'achievements': achievements[:10],
        'total_score': total_score,
        'score_by_cat': score_by_cat,
        'stats': stats,
        'rank': rank,
        'form': form,
        'cat_labels': {
            'hackathon': '🏆 Hackathon',
            'research': '📄 Research',
            'patent': '💡 Patent',
            'certificate': '🎓 Certificate',
        }
    }
    return render(request, 'spms/student_dashboard.html', context)


@login_required
def my_submissions(request):
    if request.user.role != 'student':
        return HttpResponseForbidden()
    achievements = request.user.achievements.all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        achievements = achievements.filter(status=status_filter)
    return render(request, 'spms/my_submissions.html', {
        'achievements': achievements,
        'status_filter': status_filter
    })


@login_required
def delete_achievement(request, pk):
    ach = get_object_or_404(Achievement, pk=pk, student=request.user)
    if ach.status == 'pending':
        ach.delete()
        messages.success(request, 'Achievement deleted.')
    else:
        messages.error(request, 'Cannot delete a verified achievement.')
    return redirect('my_submissions')


# ─────────────────────────────────────────────
# FACULTY VIEWS
# ─────────────────────────────────────────────

@login_required
def faculty_dashboard(request):
    if request.user.role not in ('faculty', 'admin'):
        return HttpResponseForbidden()

    pending = Achievement.objects.filter(status='pending').order_by('-submitted_at')
    approved_this_month = Achievement.objects.filter(
        status='approved',
        reviewed_at__month=timezone.now().month
    ).count()

    # Leaderboard
    students = User.objects.filter(role='student')
    leaderboard = sorted(students, key=lambda u: u.get_total_score(), reverse=True)[:10]

    stats = {
        'pending': pending.count(),
        'approved_month': approved_this_month,
        'total_students': User.objects.filter(role='student').count(),
        'avg_score': round(
            sum(u.get_total_score() for u in students) / max(students.count(), 1)
        ),
    }

    context = {
        'pending': pending[:20],
        'leaderboard': leaderboard,
        'stats': stats,
    }
    return render(request, 'spms/faculty_dashboard.html', context)


@login_required
def review_achievement(request, pk):
    if request.user.role not in ('faculty', 'admin'):
        return HttpResponseForbidden()

    ach = get_object_or_404(Achievement, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('faculty_remarks', '')
        ach.faculty_remarks = remarks
        ach.reviewed_by = request.user
        ach.reviewed_at = timezone.now()

        if action == 'approve':
            ach.status = 'approved'
            ach.auto_assign_points()
            ach.save()
            messages.success(request, f'Approved! {ach.points_awarded} pts awarded to {ach.student.get_full_name()}.')
        elif action == 'reject':
            ach.status = 'rejected'
            ach.points_awarded = 0
            ach.save()
            messages.warning(request, f'Achievement rejected.')
        return redirect('faculty_dashboard')

    return render(request, 'spms/review_achievement.html', {'ach': ach})


# ─────────────────────────────────────────────
# ADMIN VIEWS
# ─────────────────────────────────────────────

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden()

    students = User.objects.filter(role='student')
    faculty = User.objects.filter(role='faculty')
    achievements = Achievement.objects.all()

    # Category breakdown
    cat_counts = {}
    for cat, _ in Achievement.CATEGORY_CHOICES:
        cat_counts[cat] = achievements.filter(category=cat).count()
    total_ach = achievements.count() or 1

    # Leaderboard
    leaderboard = sorted(students, key=lambda u: u.get_total_score(), reverse=True)[:10]

    stats = {
        'total_students': students.count(),
        'total_faculty': faculty.count(),
        'total_submissions': achievements.count(),
        'pending': achievements.filter(status='pending').count(),
        'approved': achievements.filter(status='approved').count(),
        'avg_score': round(sum(u.get_total_score() for u in students) / max(students.count(), 1)),
    }

    context = {
        'students': students.order_by('-date_joined')[:20],
        'faculty_list': faculty,
        'leaderboard': leaderboard,
        'stats': stats,
        'cat_counts': cat_counts,
        'total_ach': total_ach,
        'point_rules': PointRule.objects.all(),
        'recent_achievements': achievements[:15],
    }
    return render(request, 'spms/admin_dashboard.html', context)


@login_required
def manage_users(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden()
    users = User.objects.all().order_by('-date_joined')
    q = request.GET.get('q', '')
    if q:
        users = users.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(enrollment_no__icontains=q) | Q(email__icontains=q)
        )
    return render(request, 'spms/manage_users.html', {'users': users, 'q': q})


@login_required
def toggle_user_active(request, pk):
    if request.user.role != 'admin':
        return HttpResponseForbidden()
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User {user.get_full_name()} has been {status}.')
    return redirect('manage_users')


@login_required
def leaderboard(request):
    students = User.objects.filter(role='student', is_active=True)
    ranked = sorted(students, key=lambda u: u.get_total_score(), reverse=True)
    dept_filter = request.GET.get('dept', '')
    if dept_filter:
        ranked = [u for u in ranked if u.department == dept_filter]
    departments = students.values_list('department', flat=True).distinct()
    return render(request, 'spms/leaderboard.html', {
        'ranked': ranked,
        'departments': departments,
        'dept_filter': dept_filter,
    })
