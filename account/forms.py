from django import forms
from .models import User, ProfileIcon
from django.contrib.auth.forms import UserCreationForm




class SignUpForm(UserCreationForm):
    GENDER = (
        ('male','Male'),
        ('female','Female')
    )
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    gender      =   forms.ChoiceField(choices=GENDER)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    mobile_number = forms.CharField(max_length=30, required=False, help_text='Optional')

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'mobile_number',
            'gender',
            'email', 
            'password1', 
            'password2', 
            ]
        



from django import forms
from .models import User, ProfileIcon
from .widgets import ImageRadioSelect


class ProfileIconSelectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_icon'].choices = [
            (icon.pk, icon.image.url)  # Store image URLs in choices
            for icon in ProfileIcon.objects.all()
        ]
        self.fields['selected_icon'].widget = ImageRadioSelect(choices=self.fields['selected_icon'].choices)

    class Meta:
        model = User
        fields = ['selected_icon']
