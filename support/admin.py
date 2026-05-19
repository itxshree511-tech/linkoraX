from django.contrib import admin
from .models import SupportTicket, TicketReply


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'user', 'subject', 'category', 'priority', 'status', 'created_at')
    list_filter = ('category', 'priority', 'status', 'created_at')
    search_fields = ('ticket_number', 'user__email', 'subject')
    readonly_fields = ('ticket_number', 'created_at', 'updated_at')


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'is_admin', 'created_at')
    list_filter = ('is_admin', 'created_at')
    search_fields = ('ticket__ticket_number', 'user__email')
