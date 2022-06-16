from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from . models import Profile, Project, Rateview
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsAdminOrReadOnly
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
    return render(request, 'registration/register.html', params)


@login_required(login_url="login")
def index(request):
    projects = Project.objects.all()
    return render(request, 'main/index.html', {"projects":projects})


# function for creating a new profile
def profile(request,id):
    prof = Profile.objects.get(user = id)
    return render(request,'main/profile.html',{"profile":prof})

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
    return render(request, 'main/editprofile.html', params)

# function for searching the profile
@login_required(login_url="login")
def searchproject(request):
    if 'search' in request.GET and request.GET['search']:
        title = request.GET.get("search_term")
        searchResults = Project.search_projects(title)
        message = f'name'
        params = {
            'results': searchResults,
            'message': message
        }
        return render(request, 'main/search.html', params)
    else:
        message = "You haven't searched for any projects"
    return render(request, 'main/search.html', {'message': message})

# function for adding a project
@login_required(login_url="login")
def addProject(request):
    current_user = request.user
    user_profile = Profile.objects.get(user = current_user)
    if request.method == 'POST':
        form = projectForm(request.POST,request.FILES)
        if form.is_valid:
            newProj = form.save(commit = False)
            newProj.user = user_profile
            newProj.save()
        return redirect('index')  
    else:
        form = projectForm()
    return render(request,'main/newproject.html',{'form':form})    

# function for readmore about the project
def projects(request,id):
    proj = Project.objects.get(id = id)
    return render(request,'main/readmore.html',{"projects":proj})

# function for rating and reviewing
@login_required(login_url="login")
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
            return redirect('index')
    else:
        form = RateForm()
    return render(request,"main/rate.html",{"form":form,"project":project})  

class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self,request,format = None):
        all_profile = Profile.objects.all()
        serializers = ProfileSerializer(all_profile,many = True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectList(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self,request,format = None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects,many = True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
