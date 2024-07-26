from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    if request.user.is_authenticated:
        return render(request, "mysite/dashboard.html", {"user": request.user})
    return render(request, "mysite/index.html", {})