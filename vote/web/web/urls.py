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

#for the control panel, there is no URL to it; that's on purpose, instead you're going to search one of the pages on the control panel,
#such as create election, create candidate, create ballot entry, etc. because those are all extensions of the control panel


urlpatterns = [
    path('', views.login, name='login'),
    path('admin/', admin.site.urls),
    path('registration_check/', views.registration_check, name='checkin'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('voter_login/', views.voter_login, name='voter_login'),
    path('create_candidate', views.create_candidate, name='create_candidate'),
    path('create_election', views.create_election, name='create_election'),
    path('create_ballot_entry', views.create_ballot_entry, name='create_ballot_entry'),
    path('delete_ballot_entry', views.delete_ballot_entry, name='delete_ballot_entry'),
    path('add_media_partner', views.media_page, name='add_media_partner'),
    path('list_media_partner', views.media_map, name='list_media_partner'),
    path('elections/<api_key>', views.elections, name='elections'),
    path('elections/<int:year>-<int:month>/<api_key>', views.election_details, name='election_details'),
    path('candidates/<first_name>-<last_name>-<int:year>/<api_key>', views.candidate_details, name='candidate_details'),
    path('election_selection/', views.election_selection, name='election_selection'),
    path('candidates/<api_key>', views.candidates, name='candidates'),
    path('voters/<api_key>', views.voters, name='voters'),
    path('instructions1', views.instructions1,name='instructions1'),
    path('instructions2', views.instructions2,name='instructions2'),
    path('primary_party_select', views.primary_party_select, name='primary_party_select'),
    path('voter_finished', views.voter_finished,name='voter_finished'),
    path('voter_cancelled', views.voter_cancelled,name='voter_cancelled'),
    path('vote/<int:pos_num>', views.vote, name='vote'),
    path('vote', views.vote, name='vote'),
    path('voter_exit_booth', views.voter_exit_booth, name='voter_exit_booth'),
    path('vote_record', views.vote_record, name='vote_record'),
    path('vote_records/<api_key>', views.vote_records, name='vote_records'),
    path('print_queue/<slug:key>', views.print_queue, name = 'print_queue'),
    path('already_voted/', views.already_voted, name='already_voted'),
    path('address_lookup/', views.address_lookup, name='address_lookup')
]
