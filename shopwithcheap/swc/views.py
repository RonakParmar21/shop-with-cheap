from django.shortcuts import render

# Client-side view
def INDEX(request):
    return render(request, 'client/index.html')  

# Admin panel view
def ADMININDEX(request):
    return render(request, 'admin/admin_dashboard.html')  

def ADMINLOGIN(request):
    return render(request, 'admin/admin_login.html')

def ADMINLOGOUT(request):
    return render(request, 'admin/admin_login.html')

def ADDSUBCATEGORY(request):
    return render(request, 'admin/addSubCategory.html')

def SHOWSUBCATEGORY(request):
    return render(request, 'admin/showSubCategory.html')

def EDITSUBCATEGORY(request):
    return render(request, 'admin/editSubCategory.html')

def DELETESUBCATEGORY(request):
    return render(request, 'admin/showSubCategory.html')

def ADDPRODUCT(request):
    return render(request, 'admin/addProduct.html')

def SHOWPRODUCT(request):
    return render(request, 'admin/showProduct.html')

def EDITPRODUCT(request):
    return render(request, 'admin/editProduct.html')

def DELETEPRODUCT(request):
    return render(request, 'admin/showProduct.html')
