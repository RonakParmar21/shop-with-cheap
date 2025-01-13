from django.shortcuts import render, redirect
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import JsonResponse
from .models import Subcategory
from django.conf import settings
import os

# Client-side view
def INDEX(request):
    return render(request, 'client/index.html')  

# Admin panel view
def ADMININDEX(request):
    if 'admin_email' not in request.session:
        error_message = "You need to log in first to access this page."
        return redirect('admin_login')
    if request.method == "GET":
        return render(request, 'admin/admin_dashboard.html')
    # else:
        # return render(request, 'admin')

def ADMINLOGIN(request):
    if 'admin_email' in request.session:
        return redirect('admin_login')
    
    if request.method=="POST":
        email = request.POST.get('admin_email')
        password = request.POST.get('admin_password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM swc_admin WHERE email = %s", [email])
            user = cursor.fetchone()

        if user:
            if user[2] == password:
                request.session['admin_email'] = user[2]
                return redirect('custom_admin')
            else:
                messages.error(request, 'Incorrect password.')
        else:
            messages.error(request, 'User does not exist.')

    return render(request, 'admin/admin_login.html')

def ADMINLOGOUT(request):
    if 'admin_email' in request.session:
        del request.session['admin_email']
    return redirect('admin_login')

def ADDSUBCATEGORY(request):
    if 'admin_email' not in request.session:
        return redirect('admin_login')
    
    if request.method=="POST":
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')

        query = """
            INSERT INTO swc_subcategory(category, subcategory) VALUES(%s, %s)
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [category, subcategory])

        return render(request, 'admin/addSubCategory.html', {'success':True})
    return render(request, 'admin/addSubCategory.html')

def SHOWSUBCATEGORY(request):
    if 'admin_email' not in request.session:
        return redirect('admin_login')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, category, subcategory FROM swc_subcategory")
        subcategories = cursor.fetchall()

    subcategories_list = [
        {'id': row[0], 'category': row[1], 'subcategory': row[2]} for row in subcategories
    ]
    return render(request, 'admin/showSubCategory.html', {'subcategories': subcategories_list})

def EDITSUBCATEGORY(request, subcategory_id):
    if 'admin_email' not in request.session:
        return redirect('admin_login')
    if request.method == 'POST':
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')

        # Update subcategory record using raw SQL
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE swc_subcategory
                SET category = %s, subcategory = %s
                WHERE id = %s
            """, [category, subcategory, subcategory_id])

        return redirect('admin_showsubcategory')

    # Fetch subcategory details using raw SQL
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, category, subcategory
            FROM swc_subcategory
            WHERE id = %s
        """, [subcategory_id])
        subcategory = cursor.fetchone()

    # if not subcategory:
        # return HttpResponse("Subcategory not found", status=404)

    subcategory_dict = {'id': subcategory[0], 'category': subcategory[1], 'subcategory': subcategory[2]}
    return render(request, 'admin/editSubCategory.html', {'subcategory': subcategory_dict})

def DELETESUBCATEGORY(request, subcategory_id):
    if 'admin_email' not in request.session:
        return redirect('admin_login')
    if request.method == 'POST':
        # Delete subcategory record using raw SQL
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM swc_subcategory
                WHERE id = %s
            """, [subcategory_id])

        return redirect('admin_showsubcategory')
    return render(request, 'admin/showSubCategory.html')

def ADDPRODUCT(request):
    if 'admin_email' not in request.session:
        return redirect('admin_login')
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
            INSERT INTO swc_product (category, subcategory, product_title, product_price, product_image)
            VALUES (%s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [category, subcategory, product_name, product_price, image_path])

        return render(request, 'admin/addProduct.html', {'success': True})

    # Fetch all categories
    query = "SELECT DISTINCT category FROM swc_subcategory"
    with connection.cursor() as cursor:
        cursor.execute(query)
        categories = cursor.fetchall()

    # Check if category is selected and fetch corresponding subcategories
    category_selected = request.GET.get('category', None)
    if category_selected:
        query = """
            SELECT DISTINCT subcategory 
            FROM swc_subcategory 
            WHERE category = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [category_selected])
            subcategories = cursor.fetchall()

    context = {
        'categories': [{'category': cat[0]} for cat in categories],
        'subcategories': [{'subcategory': sub[0]} for sub in subcategories],
    }

    return render(request, 'admin/addProduct.html', context)

def GET_SUBCATEGORIES(request):
    category = request.GET.get('category', None)
    subcategories = []
    
    if category:
        query = """
            SELECT DISTINCT subcategory 
            FROM swc_subcategory 
            WHERE category = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [category])
            subcategories = cursor.fetchall()
    
    return JsonResponse({'subcategories': [{'subcategory': sub[0]} for sub in subcategories]})

    # return render(request, 'admin/addProduct.html')

def SHOWPRODUCT(request):    
    if 'admin_email' not in request.session:
        return redirect('admin_login')

    # Fetch all products using raw SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, category, subcategory, product_title, product_price, product_image FROM swc_product")
        products = cursor.fetchall()

    # Map the query results to a list of dictionaries
    products_list = [
        {'id': row[0], 'category': row[1], 'subcategory': row[2], 'product_title': row[3], 'product_price': row[4], 'product_image': row[5]} for row in products
    ]

    return render(request, 'admin/showProduct.html', {'products': products_list})

def EDITPRODUCT(request, product_id):
    if request.method == 'POST':
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        product_title = request.POST.get('product_title')
        product_price = request.POST.get('product_price')
        product_image = request.FILES.get('product_image')

        # If new image is uploaded, save it
        if product_image:
            fs = FileSystemStorage()
            filename = fs.save(product_image.name, product_image)
            product_image_path = fs.url(filename)
        else:
            product_image_path = request.POST.get('existing_product_image')

        # Update the product record using raw SQL
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE swc_product
                SET category = %s, subcategory = %s, product_title = %s, product_price = %s, product_image = %s
                WHERE id = %s
            """, [category, subcategory, product_title, product_price, product_image_path, product_id])

        return redirect('admin_showproduct')

    # Fetch the selected product for editing
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, category, subcategory, product_title, product_price, product_image
            FROM swc_product
            WHERE id = %s
        """, [product_id])
        product = cursor.fetchone()

    # Fetch all categories and subcategories
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT category FROM swc_subcategory")
        categories = cursor.fetchall()

    # Fetch subcategories based on the selected category
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT subcategory 
            FROM swc_subcategory 
            WHERE category = %s
        """, [product[1]])  # Pass the current product's category
        subcategories = cursor.fetchall()

    product_dict = {'id': product[0], 'category': product[1], 'subcategory': product[2], 'product_title': product[3], 'product_price': product[4], 'product_image': product[5]}

    context = {
        'product': product_dict,
        'categories': [{'category': cat[0]} for cat in categories],
        'subcategories': [{'subcategory': sub[0]} for sub in subcategories],
    }

    return render(request, 'admin/editProduct.html', context)

def DELETEPRODUCT(request, product_id):
    if 'admin_email' not in request.session:
        return redirect('admin_login')
    if request.method == 'POST':
        # Delete subcategory record using raw SQL
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM swc_product
                WHERE id = %s
            """, [product_id])

        return redirect('admin_showproduct')
    return render(request, 'admin/showProduct.html')
