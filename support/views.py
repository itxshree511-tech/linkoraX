from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SupportTicket, TicketReply
from .forms import SupportTicketForm, TicketReplyForm


@login_required
def support_view(request):
    tickets = SupportTicket.objects.filter(user=request.user)
    
    context = {
        'tickets': tickets,
    }
    return render(request, 'dashboard/support.html', context)


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Support ticket created successfully.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = SupportTicketForm()
    
    return render(request, 'dashboard/create_ticket.html', {'form': form})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    replies = ticket.replies.all()
    
    if request.method == 'POST':
        form = TicketReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.user = request.user
            reply.is_admin = False
            reply.save()
            messages.success(request, 'Reply sent successfully.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketReplyForm()
    
    context = {
        'ticket': ticket,
        'replies': replies,
        'form': form,
    }
    return render(request, 'dashboard/ticket_detail.html', context)
