from django.shortcuts import render

# client side views 
def Index(request):
    return render(request, "client/index.html")

def Login(request):
    if request.method == "GET":
        return render(request, "client/login.html")
    if request.method == "POST":
        return render(request, "swc/login.html")

def AdminLogin(request):
    return render(request, "swc/login.html")
