from django.http import JsonResponse
import os
from django.conf import settings
from django.db import connection
from django.shortcuts import render

# client side views 
from django.db import connection
from django.shortcuts import render

def Index(request):
    # Fetch 6 random products from the database
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.productname, p.productdescription, p.productprice, p.productimage, p.category, p.subcategory
            FROM product p
            ORDER BY RAND() LIMIT 6
        """)
        products_data = cursor.fetchall()

        # Prepare the products data
        products = [
            {
                'name': row[0],           # Product name (index 0)
                'description': row[1],    # Product description (index 1)
                'price': row[2],          # Product price (index 2)
                'image': row[3],          # Product image (index 3)
                'category': row[4],       # Category name (index 4)
                'subcategory': row[5],    # Subcategory name (index 5)
            } for row in products_data
        ]

    # Fetch categories and subcategories
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

    return render(request, 'client/index.html', {'products': products, 'categories': categories})

# def Index(request):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM product ORDER BY RAND() LIMIT 6")
#         product = cursor.fetchall()
#         products = [
#             {
#                 'name': row[1],
#                 'description': row[4],
#                 'price': row[5],
#                 'image': row[7],
#             } for row in product
#         ]
#     return render(request, 'client/index.html', {'products': products})


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

def Contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')

        with connection.cursor() as cursor:
            sql = "INSERT INTO contact(name, email, mobile, message) VALUES('"+name+"', '"+email+"', '"+mobile+"', '"+message+"')"
            cursor.execute(sql)
            message = "Contact message sent successfully..."
        return render(request, "client/contact.html", {'message': message})
    return render(request, "client/contact.html")

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
        cursor.execute("SELECT categoryname FROM category")
        categories = cursor.fetchall()  # Returns a list of tuples

    categories_list = [category[0] for category in categories]
    if request.method=="POST":
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')

        query = "INSERT INTO subcategory(category, subcategory) VALUES('"+category+"', '"+subcategory+"')"

        with connection.cursor() as cursor:
            cursor.execute(query)

        return render(request, 'swc/addsubcategory.html', {'categories': categories_list, 'success': True})

    return render(request, 'swc/addsubcategory.html', {'categories': categories_list})

def AddProduct(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT categoryname FROM category")
        categories = cursor.fetchall()

    categories_list = [category[0] for category in categories]

    if request.method == "POST":
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        product_name = request.POST.get('product_name')
        productdescription = request.POST.get('productdescription')
        productprice = request.POST.get('productprice')
        productqty = request.POST.get('productqty')
        productimage = request.FILES.get('productimage')

        if productimage:
            image_folder = os.path.join(settings.IMAGE_STORAGE_PATH, 'product')
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
    return render(request, 'swc/addproduct.html', {'categories': categories_list})

def get_subcategories(request):
    if request.method == "GET":
        category = request.GET.get('category')

        with connection.cursor() as cursor:
            cursor.execute("SELECT subcategory FROM subcategory WHERE category = %s", [category])
            subcategories = cursor.fetchall()

        subcategories_list = [subcategory[0] for subcategory in subcategories]
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
    return render(request, "swc/viewproduct.html", {"products":product_list})

def ViewContactDetails(request):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM contact"
        cursor.execute(sql)
        contact = cursor.fetchall()
        contact_list = [
            {
                'name':row[0],
                'email':row[1],
                'mobile':row[2],
                'message':row[3]
            } for row in contact
        ]
        return render(request, "swc/viewcontactdetails.html", {"contacts":contact_list})
    

def search_products(request):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')

    query = "SELECT * FROM product p"
    conditions = []
    params = []

    # Add conditions to the query if category or subcategory is provided
    if category:
        conditions.append("p.category = %s")
        params.append(category)
    
    if subcategory:
        conditions.append("p.subcategory = %s")
        params.append(subcategory)

    # If there are conditions, add them to the query
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        products_data = cursor.fetchall()

    # Prepare the products data
    products = [
        {
            'name': row[4],           # Product name (index 4)
            'description': row[1],    # Product description (index 1)
            'price': row[2],          # Product price (index 2)
            'image': row[3],          # Product image (index 3)
            'category': row[4],       # Category (index 4)
            'subcategory': row[5],    # Subcategory (index 5)
        } for row in products_data
    ]

    return render(request, 'client/index.html', {'products': products})

def SearchProducts(request):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')

    # Base query to fetch products
    query = "SELECT * FROM product p"
    conditions = []
    params = []

    # Add conditions for filtering by category and subcategory
    if category:
        conditions.append("p.category = %s")
        params.append(category)

    if subcategory:
        conditions.append("p.subcategory = %s")
        params.append(subcategory)

    # Add conditions to query if any exist
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        products_data = cursor.fetchall()

    # Prepare the product data to be passed to the template
    products = [
        {
            'name': row[4],           # Product name (index 4)
            'description': row[1],    # Product description (index 1)
            'price': row[5],          # Product price (index 2)
            'image': row[7],          # Product image (index 3)
            'category': row[4],       # Category (index 4)
            'subcategory': row[5],    # Subcategory (index 5)
        } for row in products_data
    ]

    # Fetch categories and subcategories for the navbar
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.categoryname, s.subcategory
            FROM category c
            LEFT JOIN subcategory s ON c.categoryname = s.category
            ORDER BY c.categoryname, s.subcategory
        """)
        categories_data = cursor.fetchall()

    # Prepare the categories dictionary
    categories = {}
    for row in categories_data:
        category_name = row[0]
        subcategory_name = row[1]
        if category_name not in categories:
            categories[category_name] = []
        if subcategory_name:
            categories[category_name].append(subcategory_name)

    # Return the products and categories to the template
    return render(request, 'client/searchedproduct.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'selected_subcategory': subcategory
    })

def ProductDetail(request, product_id):
    with connection.cursor() as cursor:
        # Query the product details by product ID
        cursor.execute("""
            SELECT p.id, p.productname, p.productdescription, p.productprice, p.productimage, p.category, p.subcategory
            FROM product p
            WHERE p.id = %s
        """, [product_id])
        product_data = cursor.fetchone()

    if product_data:
        product = {
            'id': product_data[0],
            'name': product_data[1],
            'description': product_data[2],
            'price': product_data[3],
            'image': product_data[4],
            'category': product_data[5],
            'subcategory': product_data[6],
        }
    else:
        product = None

    # Pass the product data to the template
    return render(request, 'client/productDetail.html', {'product': product})