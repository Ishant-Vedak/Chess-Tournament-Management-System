from django.urls import path
from . import views

app_name = "tournaments"
urlpatterns = [
    path("", views.tournament, name="tournament"),
    path("all/", views.all_tournaments, name="all_tournaments"),
    path('all/<uuid:uuid>/', views.tournament_details, name='tournament_details'),
    path("create/", views.create_tournament, name="create_tournament"),
    path("my_tournaments/", views.my_tournaments, name="my_tournaments"),
    path('create/confirm/', views.confirm_tournament, name='confirm_tournament'),
    path('<uuid:uuid>/join_tournament/', views.join_tournament, name='join_tournament'),

    #Tournament Admin

    #Admin Page of Tournament.
    path('<uuid:uuid>/admin/', views.tournament_admin, name='tournament_admin'),
    #Tournament Settings Page.
    path('<uuid:uuid>/settings/', views.tournament_settings, name='tournament_settings'),
    #Page that everyone else sees.
    path('<uuid:uuid>/', views.main_tournament_page, name='main_tournament_page'),
    #Page showing all participants.
    path('<uuid:uuid>/all_participants/', views.all_participants_in_tournament, name='all_participants'),
    #Confirmation Page before starting Tournament.
    path('<uuid:uuid>/start/', views.start_tournament, name='start_tournament'),

    
    #Hosting Tournament

    # Round for a Tournament.
    path('<uuid:uuid>/<int:round_num>/', views.hosting_tournament_round, name='tournament_round'),
    # End of round for a Tournament, showing the total points of all participants.
    path('<uuid:uuid>/<int:round_num>/end', views.end_tournament_round, name='round_end'),
    # End of Tournament, showing the rankings of people, who won, and should give a document to download at the end.
    path('<uuid:uuid>/end/', views.tournament_end, name='tournament_end'),
]

# Planned URLs:
#path('<uuid:uuid>/<int:round_number>/') #This will be the page for each round. The round number variable will come from another model, probably called HostTournaments.