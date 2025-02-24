from django import forms
from .models import Varient, Clan, ClanCredit, ClanPaymentLoan, ClanSettings
from django.contrib.auth import get_user_model

User = get_user_model()

class ClanCreateForm(forms.Form):
    name = forms.CharField(max_length=50)




class SavingForm(forms.Form):
    def __init__(self, clan, *args, **kwargs):
        super(SavingForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(varient__clan=clan)
        self.fields['amount'].widget.attrs['placeholder'] = 'Enter amount'
    
    user = forms.ModelChoiceField(queryset=User.objects.none())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)




class ClanApplyLoan(forms.Form):
    PERIOD = (
        (12,'1 Week'),
        (20, '2 Weeks'),
        (25, '25% 1Month'),
        (30, '1 Month'),
        (40,'8 Weeks'),
        (50, '16 Weeks')
    )
    amount  =  forms.DecimalField(max_digits=10, decimal_places=2)
    period      = forms.ChoiceField(
        choices=PERIOD,
        widget=forms.Select(
            attrs={
                'class': 'custom-select',
                'placeholder': 'Choose a color'
            }
        )
    )

class LoanPaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


class ShowTotalSavingsForm(forms.ModelForm):
    class Meta:
        model = Varient
        fields = ['show_saving']


class ClanUpdateForm(forms.ModelForm):
    class Meta:
        model = Clan
        fields = ['name','interest', 'location']




class ClanSettingsForm(forms.ModelForm):
    class Meta:
        model = ClanSettings
        fields = ['minimum_in_savings_for_credit', 'max_members', 'who_can_see_credits']
        widgets = {
            'minimum_in_savings_for_credit': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_members': forms.NumberInput(attrs={'class': 'form-control'}),
            'who_can_see_credits': forms.Select(attrs={'class': 'form-control'}),
        }
