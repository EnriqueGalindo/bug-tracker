from custom_user.models import MyCustomUser
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import LoginForm
from tickets.forms import TicketForm
from tickets.models import Ticket
from django.contrib.auth.decorators import login_required


def login_view(request):
    html = "genericForm.html"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data["username"],
                                password=data["password"])
            if user:
                login(request, user)
                return redirect(request.GET.get("next", "/"))
            else:
                return HttpResponse("invalid authentication")

    form = LoginForm()

    return render(request, html, {'form': form})

@login_required
def create_ticket_view(request):
    html = 'genericForm.html'

    if request.method == 'POST':
        form = TicketForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                title=data['title'],
                description=data['description'],
                filed_by=request.user
            )
            return redirect(request.GET.get("next", "/"))
    
    form = TicketForm()

    return render(request, html, {'form': form})
