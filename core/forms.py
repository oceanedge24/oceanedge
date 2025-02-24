from django import forms

from .models import PayLoan




class ApplyLoanForm(forms.Form):
    PERIOD = (
        (12,'1 Week'),
        (20, '2 Weeks'),
        (25, '25% 1Month'),
        (30, '1 Month'),
        (40,'8 Weeks'),
        (50, '16 Weeks')
    )
    amount      = forms.DecimalField(max_digits=10, decimal_places=2)
    period      = forms.ChoiceField(
        choices=PERIOD,
        widget=forms.Select(
            attrs={
                'class': 'custom-select',
                'placeholder': 'Choose a color'
            }
        )
    )
    witness =   forms.CharField(max_length=20)


class LoanPaymentForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        model  = PayLoan
        fields = ('amount',)