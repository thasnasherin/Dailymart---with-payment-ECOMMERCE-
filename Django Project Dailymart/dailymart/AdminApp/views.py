from django.shortcuts import render,redirect
from . models import *
from UserApp . models import *
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def adminindex(request):
    products = Products.objects.all().count()
    category = Category.objects.all().count()
    users = Register.objects.all().count()
    messages = Contact.objects.all().count()
    orders = Checkout.objects.all().count()
    return render(request,'adminindex.html',{'products':products,'category':category,'users':users,'messages':messages,'orders':orders})
def addcategory(request):
    return render(request,'addcategory.html')
def addcat(request):
    if request.method == 'POST':
        cat_name = request.POST.get('cat_name')
        cat_desc = request.POST.get('cat_desc')
        cat_img = request.FILES.get('cat_img')
        data = Category(category_name = cat_name, category_desc = cat_desc, category_image = cat_img)
        data.save()
    return redirect('viewcategory')
def delcat(request,id):
    data = Category.objects.get(id=id).delete()
    return redirect('viewcategory')
def addproducts(request):
    data = Category.objects.all()
    return render(request,'addproducts.html',{'data':data})
def addpro(request):
    if request.method == 'POST':
        pro_name = request.POST.get('product_name')
        pro_desc = request.POST.get('product_desc')
        pro_price = request.POST.get('product_price')
        pro_img = request.FILES.get('product_image')
        pro_cat = request.POST.get('product_cat')
        data = Products(product_name = pro_name, product_desc = pro_desc, product_price = pro_price,product_image=pro_img,product_category=pro_cat)
        print(pro_cat)
        data.save()
    return redirect('viewproducts')
def delproducts(request,id):
    data = Products.objects.get(id=id).delete()
    return redirect('viewproducts')
def viewcategory(request):
    data = Category.objects.all()
    return render(request,'viewcategory.html',{'data':data})
def viewproducts(request):
    data = Products.objects.all()
    return render(request,'viewproducts.html',{'data':data})
def viewuser(request):
    data = Register.objects.filter(status = 0)
    data1 = Register.objects.filter(status = 1)
    data2 = Register.objects.filter(status = 2)
    return render(request,'viewusers.html',{'data':data,'data1':data1,'data2':data2})
def viewcontact(request):
    data = Contact.objects.all()
    return render(request,'viewcontact.html',{'data':data})
def editcat(request,id):
    data = Category.objects.filter(id=id)
    return render(request,'editcat.html',{'data':data})
def editproducts(request,id):
    data = Products.objects.filter(id=id)
    data1 = Category.objects.all()
    return render(request,'editproducts.html',{'data':data,'data1':data1})


def updateproduct(request,id):
    if request.method == 'POST':
        pro_name = request.POST.get('product_name')
        pro_desc = request.POST.get('product_desc')
        pro_price = request.POST.get('product_price')
        pro_category = request.POST.get('product_cat')
        try:
            pro_img = request.FILES.get('product_image')
            fs = FileSystemStorage()
            pro_img = fs.save(pro_img.name,pro_img)
        except MultiValueDictKeyError:
            pro_img = Products.objects.get(id=id).product_image
        Products.objects.filter(id=id).update(product_name = pro_name, product_price = pro_price, product_desc = pro_desc,product_category = pro_category,product_image = pro_img)
    return redirect('viewproducts')

def updatecat(request,id):
    if request.method == 'POST':
        cat_name = request.POST.get('cat_name')
        cat_desc = request.POST.get('cat_desc')
        try:
            cat_img = request.FILES.get('cat_img')
            fs = FileSystemStorage()
            cat_img = fs.save(cat_img.name,cat_img)
        except MultiValueDictKeyError:
            cat_img = Category.objects.get(id=id).category_image
        Category.objects.filter(id=id).update(category_name = cat_name,category_image = cat_img,category_desc = cat_desc)
    return redirect('viewcategory')
def accept(request,id):
    Register.objects.filter(id=id).update(status = 1)
    return redirect('viewuser')
def reject(request,id):
    Register.objects.filter(id=id).update(status = 2)
    return redirect('viewuser')
def vieworders(request):
    data = Checkout.objects.all()
    return render(request,'vieworders.html',{'data':data})
def delmessage(request,id):
    Contact.objects.filter(id=id).delete()
    return redirect('viewcontact')




