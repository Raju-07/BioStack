from django import forms
from django.contrib.auth import authenticate,get_user_model
from django.core.validators import RegexValidator

from .models import User,UserDetail

User = get_user_model()

class SignupForm(forms.ModelForm):
    
    username = forms.CharField(label="Username",max_length=150,validators=[RegexValidator(regex=r'^[\w-]+$',message='Username can only contain letters, numbers, underscores, and hyphens (no spaces).',code='invalid_username')],widget=forms.TextInput(attrs={'placeholder': 'Choose a unique username','class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500'}))
    email = forms.EmailField(label="Email Address",widget=forms.EmailInput(attrs={'placeholder': 'name@example.com','class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500'}))
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'placeholder': 'Create a strong password','class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500'}))
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password','class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500'}))

    class Meta:
        model = User
        fields = ("username", "email")

    # --- Validation Logic ---
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match") # Add error specifically to the field

        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower()

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if user.username:
            user.username = user.username.lower()
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")
            cleaned_data["user"] = user

        return cleaned_data
    

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        exclude = ('user',)
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style all fields to match your dashboard theme
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full bg-[#0F172A] border border-white/10 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 transition placeholder-slate-500'
            })
