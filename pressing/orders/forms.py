from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from django.contrib.auth.models import User
from .models import Contact
from .models import ChatMessage




class RegistrationForm(UserCreationForm):
    ROLES = [
        ('client', 'Client'),
        ('pressing_manager', 'Pressing Manager'),
    ]
    role = forms.ChoiceField(choices=ROLES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()



from .models import PressingProfile, Photo, Video


class PressingProfileForm(forms.ModelForm):
    class Meta:
        model = PressingProfile
        fields = [
            'business_name', 
            'location', 
            'services_offered', 
            'pricing', 
            'photos', 
            'videos', 
            'about_us', 
            'pressing_count'  # Include the new field here
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'services_offered': forms.Textarea(attrs={'class': 'form-control'}),
            'pricing': forms.Textarea(attrs={'class': 'form-control'}),
            'about_us': forms.Textarea(attrs={'class': 'form-control'}),
            'pressing_count': forms.NumberInput(attrs={'class': 'form-control'}),  # Added widget for new field
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_file']






class ReplyForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your reply here...'}))


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'description', 'service_rate', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }



class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Type your message here...'}),
        }


from .models import PressingProfile

class PromotionForm(forms.ModelForm):
    class Meta:
        model = PressingProfile
        fields = ['photos', 'videos']

class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = PressingProfile
        fields = ['facebook_url', 'instagram_url', 'tiktok_url', 'youtube_url']