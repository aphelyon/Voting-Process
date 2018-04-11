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
    path('', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('admin/', admin.site.urls),
    path('registration_check/', views.registration_check, name='checkin'),
    path('voter_registered/', views.voter_registered, name='registered'),
    path('voter_not_registered/', views.voter_not_registered, name='notregistered'),
    path('login/', views.login, name='login'),
    #path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path('voter_login/', views.voter_login, name='voter_login'),
    path('create_candidate', views.create_candidate, name='create_candidate'),
    path('create_election', views.create_election, name='create_election'),
    path('create_ballot_entry', views.create_ballot_entry, name='create_ballot_entry'),
    path('elections', views.elections, name='elections'),
    path('elections/<int:year>-<int:month>/', views.election_details, name='election_details'),
    path('candidates/<first_name>-<last_name>-<int:year>/', views.candidate_details, name='candidate_details'),
    path('election_selection/', views.election_selection, name='election_selection'),
    path('candidates', views.candidates, name='candidates'),
    path('instructions1', views.instructions1,name='instructions1'),
    path('instructions2', views.instructions2,name='instructions2'),
    path('overview', views.overview,name='overview'),
    path('voter_finished', views.voter_finished,name='voter_finished'),
    path('vote', views.vote,name='vote')
]
