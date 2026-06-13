from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    enrollment_no = models.CharField(max_length=20, blank=True, null=True, unique=True)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    def get_total_score(self):
        return sum(
            a.points_awarded for a in self.achievements.filter(status='approved')
        )

    def get_score_by_category(self):
        cats = {}
        for a in self.achievements.filter(status='approved'):
            cats[a.category] = cats.get(a.category, 0) + a.points_awarded
        return cats


class PointRule(models.Model):
    CATEGORY_CHOICES = [
        ('hackathon', 'Hackathon'),
        ('research', 'Research Paper'),
        ('patent', 'Patent'),
        ('certificate', 'Certificate'),
    ]
    LEVEL_CHOICES = [
        ('international', 'International'),
        ('national', 'National'),
        ('state', 'State'),
        ('college', 'College'),
        ('any', 'Any'),
    ]
    RESULT_CHOICES = [
        ('winner', 'Winner'),
        ('runner_up', 'Runner Up'),
        ('participation', 'Participation'),
        ('published_indexed', 'Published (Indexed)'),
        ('published_conference', 'Published (Conference)'),
        ('granted', 'Granted'),
        ('filed', 'Filed'),
        ('premium', 'Premium (AWS/Google/MS)'),
        ('standard', 'Standard (NPTEL/Coursera)'),
        ('any', 'Any'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='any')
    result = models.CharField(max_length=30, choices=RESULT_CHOICES, default='any')
    points = models.PositiveIntegerField()
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-points']

    def __str__(self):
        return f"{self.get_category_display()} | {self.get_result_display()} = {self.points} pts"


class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('hackathon', 'Hackathon'),
        ('research', 'Research Paper'),
        ('patent', 'Patent'),
        ('certificate', 'Certificate'),
    ]
    LEVEL_CHOICES = [
        ('international', 'International'),
        ('national', 'National'),
        ('state', 'State'),
        ('college', 'College'),
    ]
    RESULT_CHOICES = [
        ('winner', 'Winner'),
        ('runner_up', 'Runner Up'),
        ('participation', 'Participation'),
        ('published_indexed', 'Published (Indexed)'),
        ('published_conference', 'Published (Conference)'),
        ('granted', 'Granted'),
        ('filed', 'Filed'),
        ('premium', 'Premium (AWS/Google/MS)'),
        ('standard', 'Standard (NPTEL/Coursera)'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='achievements',
        limit_choices_to={'role': 'student'}
    )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='national')
    result = models.CharField(max_length=30, choices=RESULT_CHOICES)
    description = models.TextField(blank=True)
    proof_document = models.FileField(
        upload_to='proofs/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        blank=True, null=True
    )
    date_of_achievement = models.DateField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    points_awarded = models.PositiveIntegerField(default=0)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_achievements', limit_choices_to={'role__in': ['faculty', 'admin']}
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    faculty_remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.get_full_name()} — {self.title}"

    def auto_assign_points(self):
        """Find the best matching PointRule and assign points."""
        # Try exact match first, then fallback
        queries = [
            {'category': self.category, 'level': self.level, 'result': self.result},
            {'category': self.category, 'result': self.result, 'level': 'any'},
            {'category': self.category, 'level': self.level, 'result': 'any'},
            {'category': self.category, 'level': 'any', 'result': 'any'},
        ]
        for q in queries:
            rule = PointRule.objects.filter(**q).first()
            if rule:
                self.points_awarded = rule.points
                return rule.points
        self.points_awarded = 0
        return 0

    def get_category_icon(self):
        icons = {
            'hackathon': '🏆',
            'research': '📄',
            'patent': '💡',
            'certificate': '🎓',
        }
        return icons.get(self.category, '📋')
