from django.shortcuts import render, reverse, HttpResponseRedirect
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
    data = Ticket.objects.filter(ticket_status=Ticket.New).order_by("-time")
    in_progress = Ticket.objects.filter(
                                        ticket_status=Ticket.In_Progress
                                        ).order_by("-time")
    done = Ticket.objects.filter(ticket_status=Ticket.Done).order_by("-time")
    invalid = Ticket.objects.filter(
                                    ticket_status=Ticket.Invalid
                                    ).order_by("-time")
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


def login_view(request):
    html = 'generic_form.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginForm()

    return render(request, html, {'form': form})


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
                data['username'], data['first_name'], data['password1']
            )
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = RegisterForm()
    return render(request, html, {'form': form})


@login_required
def create_ticket_view(request):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = TicketForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                title=data['title'],
                description=data['description'],
                user_name=request.user
            )
            return HttpResponseRedirect(reverse('home'))
    else:
        form = TicketForm()

    return render(request, html, {'form': form})


@login_required
def edit_ticket_view(request, id):
    html = 'generic_form.html'

    if request.method == 'POST':
        form = EditTicket(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.filter(id=id).update(
                status='In Progress',
                assigned_to=data['assigned_to']
            )
            return HttpResponseRedirect(reverse('home'))
    else:
        form = EditTicket()

    return render(request, html, {'form': form})


@login_required
def completed_ticket_view(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.assigned_user = None
    ticket.completed_user = request.user
    ticket.ticket_status = 'Done'
    ticket.save()
    return HttpResponseRedirect(reverse('home'))


@login_required
def invalid_ticket_view(request, id):

    ticket = Ticket.objects.get(id=id)
    ticket.assigned_user = None
    ticket.completed_user = None
    ticket.ticket_status = 'Invalid'
    ticket.save()
    return HttpResponseRedirect(reverse('home'))

