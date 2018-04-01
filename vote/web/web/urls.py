"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from web import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration_check/', views.registration_check, name='checkin'),
    path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path('voter_login/', views.voter_login, name='voter_login'),
    path('create_candidate', views.create_candidate, name='create_candidate'),
    path('create_election', views.create_election, name='create_election'),
    path('add_candidate', views.add_candidate, name='add_candidate'),
    path('elections', views.elections, name='elections'),
    path('elections/<int:year>-<int:month>/', views.election_stuff, name='election_stuff'),
    path('candidates', views.candidates, name='candidates'),
]
