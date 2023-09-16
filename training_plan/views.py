from django.shortcuts import render

def index(request):
    return render(request, "training_plan/index.html")
