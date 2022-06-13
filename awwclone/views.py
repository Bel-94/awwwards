from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from . models import Profile, Project, Rateview
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import profileForm,UserUpdateForm,RegistrationForm,projectForm,UpdateUserProfileForm,RateForm

from .serializer import ProfileSerializer, ProjectSerializer
# Create your views here.

# function for the registration form
def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        procForm=profileForm(request.POST, request.FILES)
        if form.is_valid() and procForm.is_valid():
            username=form.cleaned_data.get('username')
            user=form.save()
            profile=procForm.save(commit=False)
            profile.user=user
            profile.save()

            # messages.success(request, f'Successfully created Account!.You can now login as {username}!')
        return redirect('login')
    else:
        form= RegistrationForm()
        prof=profileForm()
    params={
        'form':form,
        'profForm': prof
    }
    return render(request, 'users/register.html', params)


def index(request):
    projects = Project.objects.all()
    return render(request,'index.html',{"projects":projects})


# function for creating a new profile
def profile(request,id):
    prof = Profile.objects.get(user = id)
    return render(request,'profile.html',{"profile":prof})

# function for updating user profile
def editprofile(request):
    user= request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.id)
    else:
        user_form = UserUpdateForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'editprofile.html', params)

# function for searching the profile
def searchprofile(request):
    if 'searchUser' in request.GET and request.GET['searchUser']:
        name = request.GET.get("searchUser")
        searchResults = Project.search_projects(name)
        message = f'name'
        params = {
            'results': searchResults,
            'message': message
        }
        return render(request, 'search.html', params)
    else:
        message = "You haven't searched for any profile"
    return render(request, 'search.html', {'message': message})

# function for adding a project
def addProject(request):
    current_user = request.user
    user_profile = Profile.objects.get(user = current_user)
    if request.method == 'POST':
        form = projectForm(request.POST,request.FILES)
        if form.is_valid:
            newProj = form.save(commit = False)
            newProj.user = user_profile
            newProj.save()
        return redirect('home')  
    else:
        form = projectForm()
    return render(request,'newProject.html',{'form':form})    

# function for readmore about the project
def projects(request,id):
    proj = Project.objects.get(id = id)
    return render(request,'readmore.html',{"projects":proj})

# function fir rating and reviewing
def rate(request,id):
    # reviews = Rateview.objects.get(projects_id = id).all()
    # print
    project = Project.objects.get(id = id)
    user = request.user
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = user
            rate.projects = project
            rate.save()
            return redirect('home')
    else:
        form = RateForm()
    return render(request,"rate.html",{"form":form,"project":project})  

class ProfileList(APIView):
    def get(self,request,format = None):
        all_profile = Profile.objects.all()
        serializerdata = ProfileSerializer(all_profile,many = True)
        return Response(serializerdata.data)

class ProjectList(APIView):
    def get(self,request,format = None):
        all_projects = Project.objects.all()
        serializerdata = ProjectSerializer(all_projects,many = True)
        return Response(serializerdata.data)
