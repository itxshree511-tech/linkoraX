from django import forms
from .models import MembershipPayment


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow the two manual wallet methods we actively support.
        self.fields['payment_method'].choices = [
            (MembershipPayment.PaymentMethod.JAZZCASH, 'JazzCash'),
            (MembershipPayment.PaymentMethod.EASYPAISA, 'Easypaisa'),
        ]

    def clean_payment_method(self):
        method = (self.cleaned_data.get('payment_method') or '').strip().lower()
        allowed = {
            MembershipPayment.PaymentMethod.JAZZCASH,
            MembershipPayment.PaymentMethod.EASYPAISA,
        }
        if method not in allowed:
            raise forms.ValidationError('Please select JazzCash or Easypaisa only.')
        return method

    def clean_transaction_id(self):
        txn = (self.cleaned_data.get('transaction_id') or '').strip()
        if len(txn) < 6:
            raise forms.ValidationError('Valid transaction ID required (minimum 6 characters).')
        exists = MembershipPayment.objects.filter(transaction_id__iexact=txn).exists()
        if exists:
            raise forms.ValidationError('This transaction ID is already used.')
        return txn

    class Meta:
        model = MembershipPayment
        fields = ['payment_method', 'transaction_id']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'transaction_id': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'placeholder': 'Enter transaction ID'}),
        }
