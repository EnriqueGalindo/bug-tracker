"""bug_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    list_ticket_view,
    detail_ticket_view,
    # login_view,
    logout_view,
    register_view,
    # create_ticket_view,
    edit_ticket_view,
    completed_ticket_view,
    invalid_ticket_view,
    users_tickets_view
)

from custom_user.views import login_view, create_ticket_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', list_ticket_view, name="home"),
    path('ticket/<int:id>/', detail_ticket_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('new_ticket/', create_ticket_view),
    path('edit/<int:id>/', edit_ticket_view),
    path('complete/<int:id>/', completed_ticket_view),
    path('invalid/<int:id>/', invalid_ticket_view),
    path('userpage/<int:id>/', users_tickets_view)
]
