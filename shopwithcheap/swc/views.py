from django.shortcuts import render, redirect # type: ignore
from django.db import connection # type: ignore
from django.contrib import messages #type: ignore
from django.http import JsonResponse #type: ignore
from django.conf import settings #type: ignore
import os

# Client side views
def Index(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM product ORDER BY RAND() LIMIT 6
        """)
        products_data = cursor.fetchall()

    products = [
        {
            'id': row[0],
            'name': row[3],           
            'description': row[4],    
            'price': row[5],         
            'image': row[7],         
            'category': row[1], 
            'subcategory': row[2],    
        } for row in products_data
    ]

    categories = get_categories() 

    return render(request, 'client/index.html', {'products': products, 'categories': categories})

def check_user_credentials(email, password):
    query = """
        SELECT * FROM user
        WHERE email = %s AND password = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [email, password])
        user = cursor.fetchone()
    return user

def Login(request):
    if 'user_email' in request.session:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = check_user_credentials(email, password)
        if user:
            request.session['user_id'] = user[0] 
            request.session['user_email'] = email 
            messages.success(request, "Login successful!")
            return redirect('home')  
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login') 
    categories = get_categories() 
    return render(request, 'client/login.html', {'categories': categories})

def Logout(request):
    if 'user_id' in request.session:
        request.session.flush()
        # del request.session['user_id']
        # del request.session['user_email']  
    return redirect('home')

def Register(request):
    if 'user_id' in request.session:
        return redirect('home')
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

def get_categories():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.categoryname, s.subcategory
            FROM category c
            LEFT JOIN subcategory s ON c.categoryname = s.category
            ORDER BY c.categoryname, s.subcategory
        """)
        categories_data = cursor.fetchall()

    categories = {}
    for row in categories_data:
        category_name = row[0]
        subcategory_name = row[1]
        if category_name not in categories:
            categories[category_name] = []
        if subcategory_name:
            categories[category_name].append(subcategory_name)

    return categories

def SearchProducts(request):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')

    query = "SELECT * FROM product p"
    conditions = []
    params = []

    if category:
        conditions.append("p.category = %s")
        params.append(category)

    if subcategory:
        conditions.append("p.subcategory = %s")
        params.append(subcategory)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        products_data = cursor.fetchall()

    products = [
        {
            'name': row[4],         
            'description': row[1],  
            'image': row[7],          
            'category': row[4],      
            'subcategory': row[5],    
        } for row in products_data
    ]

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.categoryname, s.subcategory
            FROM category c
            LEFT JOIN subcategory s ON c.categoryname = s.category
            ORDER BY c.categoryname, s.subcategory
        """)
        categories_data = cursor.fetchall()

    categories = {}
    for row in categories_data:
        category_name = row[0]
        subcategory_name = row[1]
        if category_name not in categories:
            categories[category_name] = []
        if subcategory_name:
            categories[category_name].append(subcategory_name)

    return render(request, 'client/searchedproduct.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'selected_subcategory': subcategory
    })

def product_detail(request, id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM product WHERE id = %s", [id]) 
    product = cursor.fetchone() 

    if product:
        product_qty = product[6] 
        product = {
            'id': product[0], 
            'name': product[3],  
            'description': product[4], 
            'price': product[5],  
            'productqty': product_qty,
            'image': product[7],  
        }
    if product_qty == 0:
        out_of_stock = True
    else:
        out_of_stock = False
    categories = get_categories() 
    return render(request, 'client/productDetails.html', {'product': product, 'categories': categories, 'out_of_stock': out_of_stock})

def Contact(request):
    if 'user_email' not in request.session:
        return redirect('login')
    categories = get_categories()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')

        with connection.cursor() as cursor:
            sql = "INSERT INTO contact(name, email, mobile, message) VALUES('"+name+"', '"+email+"', '"+mobile+"', '"+message+"')"
            cursor.execute(sql)
            message = "Contact message sent successfully..."
            
        return render(request, "client/contact.html", {'message': message, 'categories': categories})
    return render(request, "client/contact.html", {'categories': categories})

def add_to_cart(request, product_id):
    if 'user_email' not in request.session:
        return redirect('login')

    user_email = request.session['user_email']
    qty = int(request.POST.get('qty', 1))  

    with connection.cursor() as cursor:
        cursor.execute("SELECT productname, productprice, productqty FROM product WHERE id = %s", [product_id])
        product = cursor.fetchone()

        if not product:
            messages.error(request, "Product not found.")
            return redirect('home')

        product_name, product_price, available_stock = product

        if available_stock < qty:
            messages.error(request, "Not enough stock available.")
            return redirect('home')

        cursor.execute("SELECT id, productqty FROM cart WHERE useremail = %s AND productname = %s", [user_email, product_name])
        existing_cart_item = cursor.fetchone()

        if existing_cart_item:
            cart_id, existing_qty = existing_cart_item
            new_qty = existing_qty + qty

            if new_qty > available_stock:
                messages.error(request, "Not enough stock available for this update.")
                return redirect('cart')

            cursor.execute("UPDATE cart SET productqty = %s WHERE id = %s", [new_qty, cart_id])
            messages.info(request, "Product quantity updated in your cart.")
        else:
            cursor.execute(
                "INSERT INTO cart (productname, productqty, productprice, useremail) VALUES (%s, %s, %s, %s)",
                [product_name, qty, product_price, user_email]
            )
            messages.success(request, "Product added to cart!")

        cursor.execute("UPDATE product SET productqty = productqty - %s WHERE id = %s", [qty, product_id])

    return redirect('home')


# Admin side views
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

def AddSubCategory(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, categoryname FROM category")
        categories = cursor.fetchall()  # Returns a list of tuples

    # categories_list = [category[1] for category in categories]
    if request.method=="POST":
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')

        query = "INSERT INTO subcategory(category, subcategory) VALUES('"+category+"', '"+subcategory+"')"

        with connection.cursor() as cursor:
            cursor.execute(query)

        return render(request, 'swc/addsubcategory.html', {'categories': categories, 'success': True})

    return render(request, 'swc/addsubcategory.html', {'categories': categories})

def AddProduct(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, categoryname FROM category")
        categories = cursor.fetchall()

    if request.method == "POST":
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        product_name = request.POST.get('product_name')
        productdescription = request.POST.get('productdescription')
        productprice = request.POST.get('productprice')
        productqty = request.POST.get('productqty')
        productimage = request.FILES.get('productimage')
        if productimage:
            image_folder = os.path.join(settings.BASE_DIR, 'swc/static/images/products')
            # image_folder = os.path.join(settings.MEDIA_ROOT, 'products')  
            os.makedirs(image_folder, exist_ok=True)  
            image_path = os.path.join(image_folder, productimage.name)

            with open(image_path, 'wb') as f:
                for chunk in productimage.chunks():
                    f.write(chunk)

            image_relative_path = f'images/product/{productimage.name}'

        query = """
            INSERT INTO product (category, subcategory, productname, productdescription, productprice, productqty, productimage)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [
                category, subcategory, product_name, productdescription,
                productprice, productqty, image_relative_path
            ])
        return render(request, 'swc/addProduct.html', {'success': True})
    return render(request, 'swc/addproduct.html', {'categories': categories})

def get_subcategories(request):
    if request.method == "GET":
        category = request.GET.get('category')

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, subcategory FROM subcategory WHERE category = %s", [category])
            subcategories = cursor.fetchall()

        subcategories_list = [{'id': subcategory[0], 'name': subcategory[1]} for subcategory in subcategories]
        return JsonResponse({'subcategories': subcategories_list})

def ViewCategory(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM category")
        category = cursor.fetchall()

        category_list = [
            {
                'id': row[0],
                'category':row[1]
            } for row in category
        ]
    return render(request, "swc/viewcategory.html", {"categories":category_list})

def ViewSubCategory(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM subcategory")
        subcategory = cursor.fetchall()
        subcategory_list = [
            {
                'id':row[0],
                'category': row[1],
                'subcategory':row[2]
            } for row in subcategory
        ]
    return render(request, "swc/viewsubcategory.html", {"subcategories":subcategory_list})
    
def ViewProduct(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM product")
        product = cursor.fetchall();
        product_list = [
            {
                'id' : row[0],
                'category':row[1],
                'subcategory':row[2],
                'product':row[3],
                'description':row[4],
                'price':row[5],
                'qty':row[6],
                'image':row[7]
            } for row in product
        ]
    return render(request, "swc/viewproduct.html", {"products": product_list, "MEDIA_URL": settings.MEDIA_URL})
    # return render(request, "swc/viewProduct.html", {"products":product_list})

def ViewContactDetails(request):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM contact"
        cursor.execute(sql)
        contact = cursor.fetchall()
        contact_list = [
            {
                'id':row[0],
                'name':row[1],
                'email':row[2],
                'mobile':row[3],
                'message':row[4]
            } for row in contact
        ]
        return render(request, "swc/viewContactDetails.html", {"contacts":contact_list})
    
def DeleteContact(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM contact WHERE id = %s", [id])
        messages.success(request, "Contact deleted successfully.")

    return redirect('contactdetails')

def DeleteCategory(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM subcategory WHERE category = %s", [id])
        subcategory_count = cursor.fetchone()[0] 
        cursor.execute("SELECT COUNT(*) FROM product WHERE category = %s", [id])
        product_count = cursor.fetchone()[0]

        if subcategory_count > 0 or product_count > 0:
            messages.error(request, "Cannot delete category. It has subcategories or products.")
        else:
            cursor.execute("DELETE FROM category WHERE id = %s", [id])
            messages.success(request, "Category deleted successfully.")

    return redirect('viewcategory')

def DeleteSubCategory(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM product WHERE subcategory = %s", [id])
        product_count = cursor.fetchone()[0]

        if product_count > 0:
            messages.error(request, "Cannot delete subcategory. It has product.")
        else:
            cursor.execute("DELETE FROM subcategory WHERE id = %s", [id])
            messages.success(request, "SubCategory deleted successfully.")
    return redirect('viewsubcategory')

def DeleteProduct(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM product WHERE id = %s", [id])
        messages.success(request, "Product deleted successfully.")
    return redirect('viewproduct')