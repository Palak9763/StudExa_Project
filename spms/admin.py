from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Achievement, PointRule


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'email', 'role', 'enrollment_no', 'department', 'is_active')
    list_filter = ('role', 'department', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'enrollment_no')
    fieldsets = UserAdmin.fieldsets + (
        ('SPMS Info', {'fields': ('role', 'enrollment_no', 'department', 'phone', 'profile_pic')}),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'category', 'level', 'result', 'status', 'points_awarded', 'submitted_at')
    list_filter = ('category', 'status', 'level')
    search_fields = ('title', 'student__first_name', 'student__last_name', 'student__enrollment_no')
    readonly_fields = ('submitted_at', 'reviewed_at', 'points_awarded')
    actions = ['approve_selected', 'reject_selected']

    def approve_selected(self, request, queryset):
        from django.utils import timezone
        for ach in queryset.filter(status='pending'):
            ach.status = 'approved'
            ach.reviewed_by = request.user
            ach.reviewed_at = timezone.now()
            ach.auto_assign_points()
            ach.save()
        self.message_user(request, f'{queryset.count()} achievements approved.')
    approve_selected.short_description = 'Approve selected achievements'

    def reject_selected(self, request, queryset):
        queryset.filter(status='pending').update(status='rejected', points_awarded=0)
        self.message_user(request, f'{queryset.count()} achievements rejected.')
    reject_selected.short_description = 'Reject selected achievements'


@admin.register(PointRule)
class PointRuleAdmin(admin.ModelAdmin):
    list_display = ('category', 'level', 'result', 'points', 'description')
    list_filter = ('category', 'level')
