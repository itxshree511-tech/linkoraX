from django import forms
from .models import SupportTicket, TicketReply


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'category', 'priority', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'placeholder': 'Enter subject'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'priority': forms.Select(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'rows': 5, 'placeholder': 'Describe your issue'}),
        }


class TicketReplyForm(forms.ModelForm):
    class Meta:
        model = TicketReply
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg', 'rows': 4, 'placeholder': 'Type your reply'}),
        }
