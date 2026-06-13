from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Achievement


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'college@email.com'}))
    enrollment_no = forms.CharField(max_length=20, required=False,
        widget=forms.TextInput(attrs={'placeholder': '2021CS042'}))
    department = forms.CharField(max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Computer Science'}))
    role = forms.ChoiceField(choices=[
        ('student', 'Student'), ('faculty', 'Faculty')
    ])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'enrollment_no',
                  'department', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.enrollment_no = self.cleaned_data.get('enrollment_no') or None
        user.department = self.cleaned_data.get('department', '')
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email / Enrollment No.',
        widget=forms.TextInput(attrs={'placeholder': '2021CS042 or email@college.edu'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'})
    )


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'category', 'level', 'result',
                  'description', 'proof_document', 'date_of_achievement']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Smart India Hackathon 2025'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief description...'}),
            'date_of_achievement': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamic result choices based on category
        self.fields['result'].widget = forms.Select(choices=Achievement.RESULT_CHOICES)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['faculty_remarks']
        widgets = {
            'faculty_remarks': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add remarks (optional)...'
            })
        }
