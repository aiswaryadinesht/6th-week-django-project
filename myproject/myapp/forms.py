from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid Gmail address.")
    phone_number = PhoneNumberField(null=False, blank=False, help_text="Enter a valid phone number including country code.")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }
        help_texts = {
            'username': 'Enter a unique username. This will be your identifier.',
            'email': 'Enter your @gmail.com email address.',
            'phone_number': 'Enter your phone number, including the country code.',
            'password1': 'Password must be at least 8 characters long and contain both letters and numbers.',
            'password2': 'Enter the same password as before for verification.',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Please use your @gmail.com email address.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.is_valid():
            raise forms.ValidationError("Invalid phone number.")
        return phone_number
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
class CustomUserChangeForm(UserChangeForm):
    password = None  # Remove the password field

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }
        help_texts = {
            'username': 'Enter a unique username. This will be your identifier.',
            'email': 'Enter a valid email address.',
            'phone_number': 'Enter your phone number, including the country code.',
        }
class CustomUserPasswordChangeForm(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ('new_password1', 'new_password2')
        widgets = {
            'new_password1': forms.PasswordInput(attrs={'placeholder': 'New Password'}),
            'new_password2': forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        }
        help_texts = {
            'new_password1': 'Enter a strong password.',
            'new_password2': 'Enter the same password as above, for verification.',
        }
