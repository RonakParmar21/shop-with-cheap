from django.shortcuts import render, redirect

# Create your views here.
def INDEX(request):
    return render(request, 'client_panel/index.html')