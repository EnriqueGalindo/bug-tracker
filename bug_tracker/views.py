from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from tickets.forms import TicketForm, EditTicket
from custom_user.forms import LoginForm, RegisterForm
from custom_user.models import MyCustomUser
from tickets.models import Ticket


@login_required
def list_ticket_view(request):
    html = 'index.html'
    data = Ticket.objects.filter(status=Ticket.new).order_by("-date")
    in_progress = Ticket.objects.filter(
                                        status=Ticket.in_progress
                                        ).order_by("-date")
    done = Ticket.objects.filter(status=Ticket.done).order_by("-date")
    invalid = Ticket.objects.filter(
                                    status=Ticket.invalid
                                    ).order_by("-date")
    return render(request, html, {'data': data,
                                  'in_progress': in_progress,
                                  'done': done,
                                  'invalid': invalid
                                  })


@login_required
def detail_ticket_view(request, id):
    html = 'ticket.html'
    data = Ticket.objects.get(id=id)
    return render(request, html, {'data': data})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/home/'))


@staff_member_required
def register_view(request):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = MyCustomUser.objects.create_user(
                data['username'], data['first_name'], data['password']
            )
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = RegisterForm()
    return render(request, html, {'form': form})


@login_required
def edit_ticket_view(request, id):
    html = 'genericForm.html'

    if request.method == 'POST':
        form = EditTicket(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.filter(id=id).update(
                status='nprgs',
                assigned_to=data['assigned_to']
            )
            return redirect(request.GET.get("next", "/"))
    else:
        form = EditTicket()

    return render(request, html, {'form': form})


@login_required
def completed_ticket_view(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.assigned_user = None
    ticket.completed_user = request.user
    ticket.status = 'dn'
    ticket.save()
    return HttpResponseRedirect(reverse('home'))


@login_required
def invalid_ticket_view(request, id):

    ticket = Ticket.objects.get(id=id)
    ticket.assigned_user = None
    ticket.completed_user = None
    ticket.status = 'nvld'
    ticket.save()
    return HttpResponseRedirect(reverse('home'))


@login_required()
def users_tickets_view(request, id):
    user = None
    submitted_tickets = None
    assigned_tickets = None
    closed_tickets = None

    try:
        user = MyCustomUser.objects.get(id=id)
        submitted_tickets = Ticket.objects.filter(filed_by=user)
        assigned_tickets = Ticket.objects.filter(assigned_to=user)
        closed_tickets = Ticket.objects.filter(completed_by=user)
    except Exception as e:
        print(e)
    
    return render(request, 'userpage.html', {
        'user': user,
        'submitted_tickets': submitted_tickets,
        'assigned_tickets': assigned_tickets,
        'closed_tickets': closed_tickets
    })
