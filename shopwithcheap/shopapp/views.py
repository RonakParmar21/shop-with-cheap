from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.conf import settings
import os

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

    if request.method == "POST" and request.FILES.get('image'):
        # Handle the form submission (e.g., adding a product)
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        product_name = request.POST.get('product_name')
        productdescription = request.POST.get('productdescription')
        productprice = request.POST.get('productprice')
        productqty = request.POST.get('productqty')
        productimage = request.FILES.get('image')

        image_name = productimage.name
        image_path = os.path.join('product/', image_name)

        with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb') as f:
            for chunk in productimage.chunck():
                f.write(chunk)
        
        # continue this
        # query = """
        #     INSERT INTO swc_product (category, subcategory, product_title, product_price, product_image)
        #     VALUES (%s, %s, %s, %s, %s)
        # """
        # with connection.cursor() as cursor:
        #     cursor.execute(query, [category, subcategory, product_name, product_price, image_path])

        # return render(request, 'admin/addProduct.html', {'success': True})

        # query = "INSERT INTO product(category, subcategory, productname) VALUES(%s, %s, %s)"
        # with connection.cursor() as cursor:
        #     cursor.execute(query, [category, subcategory, product_name])

        # return render(request, 'swc/addproduct.html', {
        #     'categories': categories_list,
        #     'success': True
        # })

    return render(request, 'swc/addproduct.html', {'categories': categories_list})

def get_subcategories(request):
    if request.method == "GET":
        category = request.GET.get('category')

        with connection.cursor() as cursor:
            cursor.execute("SELECT subcategory FROM subcategory WHERE category = %s", [category])
            subcategories = cursor.fetchall()

        subcategories_list = [subcategory[0] for subcategory in subcategories]
        return JsonResponse({'subcategories': subcategories_list})
    
    