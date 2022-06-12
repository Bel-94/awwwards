from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from . models import Profile, Project, Rateview
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import profileForm,UserUpdateForm,RegistrationForm,projectForm,UpdateUserProfileForm,RateForm


# Create your views here.
def Home(request):
    return HttpResponse('Welcome')