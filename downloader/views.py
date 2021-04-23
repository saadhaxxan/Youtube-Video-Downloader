from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import youtube_dl
from .forms import DownloadForm
import re


def index(request):
    global context
    form = DownloadForm(request.POST or None)
    return render(request,'home.html',{'form':form})