from django import forms
from .models import WithdrawRequest


class WithdrawRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawRequest
        fields = ['amount', 'withdraw_method', 'account_number', 'account_holder', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'placeholder': 'Enter amount'}),
            'withdraw_method': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'account_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'placeholder': 'Account number'}),
            'account_holder': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'placeholder': 'Account holder name'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'rows': 3, 'placeholder': 'Any additional notes'}),
        }
