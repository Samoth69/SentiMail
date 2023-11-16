from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'base/index.html')

def fileuploaded(file):
    print("File: ", file, " uploaded")
    # TODO: Upload file to object storage

    # TODO: Add email to database

    
