from django.shortcuts import render
from django.db import connection

# client side views 
def Index(request):
    return render(request, "client/index.html")

def Login(request):
    if request.method == "GET":
        return render(request, "client/login.html")
    if request.method == "POST":
        return render(request, "swc/login.html")

def Register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        if password == cpassword :
            with connection.cursor() as cursor:
                sql = "INSERT INTO user (name, email, mobile, password) VALUES('"+ name +"', '"+ email +"', '"+ mobile +"', '"+ password +"')"
                cursor.execute(sql)
                message = 'Data inserted successfully!'
            return render(request, 'client/registration.html', {'message': message})
        else:
            message = 'Both password are not matched'
            return render(request, 'client/registration.html', {'message':message})

    return render(request, "client/registration.html")

def AdminLogin(request):
    return render(request, "swc/login.html")

def AdminDashboard(request):
    return render(request, "swc/dashboard.html")

def AddCategory(request):
    if request.method == "POST":
        addcategory = request.POST.get('addcategory')
        with connection.cursor() as cursor:
            sql = "INSERT INTO category(categoryname) VALUES('"+ addcategory +"')"
            cursor.execute(sql)
            message = 'Category Added Successfully'
        return render(request, 'swc/addcategory.html', {'message': message})
    
    return render(request, 'swc/addcategory.html')