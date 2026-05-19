from django import forms
from .models import MembershipPayment


class PaymentForm(forms.ModelForm):
    def clean_transaction_id(self):
        txn = (self.cleaned_data.get('transaction_id') or '').strip()
        if len(txn) < 6:
            raise forms.ValidationError('Valid transaction ID required (minimum 6 characters).')
        exists = MembershipPayment.objects.filter(transaction_id__iexact=txn).exists()
        if exists:
            raise forms.ValidationError('This transaction ID is already used.')
        return txn

    def clean_receipt_image(self):
        receipt = self.cleaned_data.get('receipt_image')
        if not receipt:
            raise forms.ValidationError('Payment receipt screenshot is required.')
        allowed_types = {'image/jpeg', 'image/png', 'image/webp'}
        if getattr(receipt, 'content_type', '') not in allowed_types:
            raise forms.ValidationError('Only JPG, PNG or WEBP images are allowed.')
        max_size = 4 * 1024 * 1024
        if receipt.size > max_size:
            raise forms.ValidationError('Receipt image size must be less than 4MB.')
        return receipt

    class Meta:
        model = MembershipPayment
        fields = ['payment_method', 'transaction_id', 'receipt_image', 'notes']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'transaction_id': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'placeholder': 'Enter transaction ID'}),
            'receipt_image': forms.FileInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'accept': 'image/png,image/jpeg,image/webp'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'rows': 3, 'placeholder': 'Any additional notes'}),
        }
