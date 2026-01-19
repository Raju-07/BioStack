from django import forms
from django.contrib.auth import authenticate

from .models import User,UserDetail


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your Password'}))

    class Meta:
        model = User
        fields = ("email",)
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
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
