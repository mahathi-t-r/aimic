from  django.urls import path
from . import views

urlpatterns =[
    path('',views.index,name='index'),
    path('login/',views. login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('search/', views.search, name='search'),
    path('library/', views.library, name='library'),
    path('search_tracks/', views.search_tracks, name='search_tracks'),
    path('feedback/', views.feedback, name='feedback'),
]