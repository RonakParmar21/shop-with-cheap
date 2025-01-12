from django.shortcuts import render, redirect # type: ignore
from django.db import connection# type: ignore
from django.shortcuts import render, redirect# type: ignore
from django.http import HttpResponse# type: ignore
from django.contrib.sessions.models import Session# type: ignore
from django.contrib import messages# type: ignore
from .models import AddCategory
from django.http import JsonResponse
import os
from django.conf import settings

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
            cursor.execute("SELECT * FROM admin_panel_user WHERE email = %s", [email])
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
    if 'user_email' not in request.session:
        error_message = "You need to log in first to access this page."
        return redirect('login')

    subcategories = []
    
    if request.method == "POST" and request.FILES.get('image'):
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        product_name = request.POST.get('product')
        product_price = request.POST.get('productprice')
        image = request.FILES.get('image')

        image_name = image.name
        image_path = os.path.join('product', image_name)

        with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Insert product into the database
        query = """
            INSERT INTO admin_panel_product (category, subcategory, product_title, product_image, product_price)
            VALUES (%s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [category, subcategory, product_name, image_path, product_price])

        return render(request, 'admin_panel/addProduct.html', {'success': True})

    # Fetch all categories
    query = "SELECT DISTINCT category FROM admin_panel_addcategory"
    with connection.cursor() as cursor:
        cursor.execute(query)
        categories = cursor.fetchall()

    # Check if category is selected and fetch corresponding subcategories
    category_selected = request.GET.get('category', None)
    if category_selected:
        query = """
            SELECT DISTINCT subcategory 
            FROM admin_panel_addcategory 
            WHERE category = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [category_selected])
            subcategories = cursor.fetchall()

    context = {
        'categories': [{'category': cat[0]} for cat in categories],
        'subcategories': [{'subcategory': sub[0]} for sub in subcategories],
    }

    return render(request, 'admin_panel/addProduct.html', context)

def GET_SUBCATEGORIES(request):
    category = request.GET.get('category', None)
    subcategories = []
    
    if category:
        query = """
            SELECT DISTINCT subcategory 
            FROM admin_panel_addcategory 
            WHERE category = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [category])
            subcategories = cursor.fetchall()
    
    return JsonResponse({'subcategories': [{'subcategory': sub[0]} for sub in subcategories]})

from .models import Product

def SHOWPRODUCT(request):
    # Check if the user is logged in
    if 'user_email' not in request.session:
        return redirect('login')
    if request.method == "GET":
        products = Product.objects.all()
        
        context = {
            'products': products,
            'user_email': request.session['user_email'],
        }
        return render(request, 'admin_panel/showProduct.html', context)

    return render(request, 'admin_panel/addProduct.html')

    # Get the selected category and subcategory (if provided)
    # selected_category = request.GET.get('category', None)
    # selected_subcategory = request.GET.get('subcategory', None)

    # # Initialize an empty queryset for products
    # products = Product.objects.all()

    # # Filter products based on the selected category and subcategory
    # if selected_category:
    #     products = products.filter(category=selected_category)

    # if selected_subcategory:
    #     products = products.filter(subcategory=selected_subcategory)

    # # Prepare the context with the products
    # context = {
    #     'products': products,  # Queryset of Product instances
    #     'user_email': request.session['user_email'],  # User email in the session
    # }

    # # Render the template with the context
    # return render(request, 'admin_panel/showProduct.html', context)


def SHOWSUBCATEGORY(request):
    if 'user_email' not in request.session:
        error_message = "You need to log in first to access this page."
        return redirect('login')
    
    if request.method == "GET":
        selected_category = request.GET.get('category', None)  # Get the category from the query parameters
        
        if selected_category:
            # Filter subcategories based on the selected category
            category = AddCategory.objects.raw("""
                SELECT DISTINCT id, subcategory 
                FROM admin_panel_addcategory 
                WHERE category = %s
            """, [selected_category])
        else:
            category = AddCategory.objects.raw("""
                SELECT DISTINCT id, subcategory 
                FROM admin_panel_addcategory
            """)
        
        context = {
            'category': category,
            'user_email': request.session['user_email'], 
        }
        
        return render(request, 'admin_panel/showSubCategory.html', context)

    # if 'user_email' not in request.session:
    #     error_message = "You need to log in first to access this page."
    #     return redirect('login')
    
    # if request.method == "GET":
    #     # category = AddCategory.objects.raw("SELECT DISTINCT * FROM admin_panel_addcategory")
    #     category = AddCategory.objects.raw("""SELECT DISTINCT id, subcategory FROM admin_panel_addcategory """)



    #     context = {
    #         'category': category,
    #         'user_email': request.session['user_email'], 
    #     }
        
    #     return render(request, 'admin_panel/showSubCategory.html', context)

    return render(request, 'admin_panel/showSubCategory.html')

def EDITSUBCATEGORY(request, id):
    if request.method == "GET":
        return render(request, "admin_panel/addSubCategory.html")
    if request.method == "POST":
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')

        with connection.cursor() as cursor:
            cursor.execute("UPDATE admin_panel_addcategory SET category=%s, subcategory=%s where id = %s", [category, subcategory, id])

        return redirect("home")
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM admin_panel_addcategory WHERE id = %s",[id])
        row = cursor.fetchone()

    if row:
        category = {
            'id':row[0],
            'category': row[1],
            'subcategory': row[2],
        }
    else :
        category={}
    context = {
        'category': category
    }
    return render(request, 'admin_panel/addSubCategory.html', context)
    