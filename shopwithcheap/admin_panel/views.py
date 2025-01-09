from django.shortcuts import render, redirect # type: ignore
from django.db import connection# type: ignore
from django.shortcuts import render, redirect# type: ignore
from django.http import HttpResponse# type: ignore
from django.contrib.sessions.models import Session# type: ignore
from django.contrib import messages# type: ignore
from .models import AddCategory

# Create your views here.
def INDEX(request):
    if 'user_email' not in request.session:
        error_message = "You need to log in first to access this page."
        return redirect('login')
    if request.method == "GET":
        return render(request, 'admin_panel/index.html')

def LOGIN(request):
    if 'user_email' in request.session:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user exists using raw SQL
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM admin_user WHERE admin_email = %s", [email])
            user = cursor.fetchone()

        if user:
            # Assuming password is the 5th field (index 4) in the table
            if user[2] == password:  # user[4] corresponds to password
                request.session['user_email'] = user[2]  # user[2] corresponds to email
                return redirect('home')
            else:
                messages.error(request, 'Incorrect password.')
        else:
            messages.error(request, 'User does not exist.')

    return render(request, 'admin_panel/login.html')

def LOGOUT(request):
    if 'user_email' in request.session:
        del request.session['user_email']
    return redirect('login')

# def ADDCATEGORY(request):
#     return render(request, 'admin_panel/addCategory.html')

def ADDSUBCATEGORY(request):
    if 'user_email' not in request.session:
        error_message = "You need to log in first to access this page."
        return redirect('login')
    
    if request.method == 'POST':
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        
        query = """
            INSERT INTO admin_panel_addcategory (category, subcategory)
            VALUES (%s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [category, subcategory])
        return render(request, 'admin_panel/addSubCategory.html', {'success': True})
    return render(request, 'admin_panel/addSubCategory.html')

def ADDPRODUCT(request):
    return render(request, 'admin_panel/addProduct.html')

def SHOWPRODUCT(request):
    return render(request, 'admin_panel/showProduct.html')

def SHOWSUBCATEGORY(request):
    if 'user_email' not in request.session:
        error_message = "You need to log in first to access this page."
        return redirect('login')
    
    if request.method == "GET":
        # category = AddCategory.objects.raw("SELECT DISTINCT * FROM admin_panel_addcategory")
        category = AddCategory.objects.raw("""SELECT DISTINCT id, subcategory FROM admin_panel_addcategory """)



        context = {
            'category': category,
            'user_email': request.session['user_email'], 
        }
        
        return render(request, 'admin_panel/showSubCategory.html', context)

    return render(request, 'admin_panel/showSubCategory.html')
