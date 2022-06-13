from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name = 'home'),
    path('search/', views.searchprofile, name='search'),
    path('newproject/',views.addProject,name = 'project'),
    path('profile/<id>/',views.profile,name = 'profile'),
    path('editprofile/',views.editprofile,name = 'editprofile'), 
    path('api/profile',views.ProfileList.as_view()),
    path('api/projects',views.ProjectList.as_view()),
    path('projects/<id>/',views.projects,name = 'projects'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('rate/<id>/',views.rate,name = 'rate')
]