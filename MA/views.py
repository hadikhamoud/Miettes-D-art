from django.shortcuts import render
from django.db import models
from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test


# Create your views here.
def homepage(request):
    return render(request,'miettes/index.html')
