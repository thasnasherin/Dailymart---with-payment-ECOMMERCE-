from django.shortcuts import render,redirect
from . models import *
from AdminApp .models import *
from django.db.models.aggregates import Sum 
import stripe
from django.conf import settings
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
from django.conf import settings

# Create your views here.
def userindex(request):
    products = Products.objects.all()
    category = Category.objects.all()
    return render(request,'userindex.html',{'products':products,'category':category})
def register(request):
    return render(request,'register.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def products(request,cat):
    if 'user_id' in request.session:
       if cat=='all':
          products = Products.objects.all()
       else:
           products=Products.objects.filter(product_category=cat)
       return render(request,'products.html',{'products':products})
    return render(request,'login.html',{'msg1':"You want to Login"})

def categories(request):
    if 'user_id' in request.session:
       category = Category.objects.all()
       return render(request,'categories.html',{'category':category})
    return render(request,'login.html',{'msg1':"You want to Login"})

def userlogin(request):
    return render(request,'login.html')
def userreg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        number = request.POST.get('number')
        place = request.POST.get('place')
        data = Register(name = name, email = email, place = place,password = password,phone = number)
        data.save()
    return redirect('userlogin')
def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if name == 'admin' and password == 'admin':
            return redirect('adminindex')
        elif Register.objects.filter(name = name,password = password,status = 1).exists():
            data = Register.objects.filter(name = name,password =password).values('id','place','email','phone').first()
            request.session['user_name'] = name
            request.session['user_password'] = password
            request.session['user_place'] = data['place']
            request.session['user_phone'] = data['phone']
            request.session['user_id'] = data['id']
            request.session['user_email'] = data['email']
            return redirect('userindex')
        else:
            return render(request,'login.html',{'msg':'invalid username or password'})
    else:
        return redirect('userlogin')
def logout(request):
    request.session.flush()
    return redirect('userlogin')
def message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        data =  Contact(name = name,email = email,subject = subject,message = message,phone = phone)
        data.save()
    return redirect('userindex')
def singledetails(request,id):
    if 'user_id' in request.session:
       product = Products.objects.filter(id = id)
       return render(request,'singledetails.html',{'product':product})
    return render(request,'login.html',{'msg1':"You want to Login"})

def cart(request):
    if 'user_id' in request.session:
       u_id = request.session.get('user_id')
       data = Cart.objects.filter(usercart = u_id,status = 0)
       a = Cart.objects.filter(usercart = u_id,status = 0).aggregate(Sum('total'))
       return render(request,'cart.html',{'data':data,'a':a})
    return render(request,'login.html',{'msg1':"You want to Login"})

def checkout(request):
    if 'user_id' in request.session:
       u_id = request.session.get('user_id')
       data = Cart.objects.filter(usercart = u_id,status = 0)
       a = Cart.objects.filter(usercart = u_id,status = 0).aggregate(Sum('total'))
       return render(request,'checkout.html',{'data':data,'a':a})
    return render(request,'login.html',{'msg1':"You want to Login"})


def payment(request):
    if 'user_id' in request.session:
       return render(request,'payment.html')
    return render(request,'login.html',{'msg1':"You want to Login"})


def paymentsuccess(request):
    if 'user_id' in request.session:
       return render(request,'paymentsuccess.html')
    return render(request,'login.html',{'msg1':"You want to Login"})


def error(request):
    if 'user_id' in request.session:
       return render(request,'error.html')
    return render(request,'login.html',{'msg1':"You want to Login"})


#----------------------------------------------------------------------------------------------------------------
#PAYPAL PAYMENT GATEWAY
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})
def create_payment(request):
    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal",
            },
            "redirect_urls": {
                "return_url": "http://127.0.0.1:8000/execute_payment",
                "cancel_url": "http://127.0.0.1:8000/error",
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Test Item",
                        "sku": "001",
                        "price": "10.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": "10.00",
                    "currency": "USD"
                },
                "description": "Test Payment"
            }]
        })

        # Attempt to create the payment on PayPal
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)  # Redirect to PayPal approval URL
        else:
            return render(request, 'error.html', {'error': payment.error})

    return render(request, 'payment.html')
# def create_payment(request):
#     if request.method == 'POST':
#         payment=paypalrestsdk.Payment({
#             "intent":"sale",
#             "payer":{
#                 "payment_method":"paypal",
#             },
#             "redirect_urls":{
#                 "return_url":"http://127.0.0.1:8000/paymentsuccess",
#                 "cancel_url":"http://127.0.0.1:8000/error",
#             },
#             "transactions":[{
#                 "items_list":{
#                     "items":[{
#                        "name":"Test Item",
#                        "sku":"001",
#                        "price":"10",
#                        "currency":"INR",
#                        "quantity":1
#                     }]
#                 },
#                 "amount":{
#                     "total":"10",
#                     "currency":"INR"
#                 },
#                 "description":"This is a test Payment"
#             }]
#         })
#         if payment.create():
#             for link in payment.links:
#                 if link.rel == "approval_url":
#                     return redirect(link.href)
#                 else:
#                     return render(request,'error.html',{'error':payment.error})
#     return render(request,'payment.html')
def execute_payment(request):
    paymentid=request.GET.get('payment_id')
    payerid=request.GET.get('payer_id')
    payment=paypalrestsdk.Payment.find(paymentid)
    if payment.execute({'payerid':payerid}):
        return render(request,'paymentsuccess.html',{'payment':payment})
    else:
        return render(request,'error.html',{'error':payment.error})

#----------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------
#STRIPE PAYMENT GATEWAY
# stripe.api_key = settings.STRIPE_API_KEY
# DOMAIN = settings.DOMAIN
# def payment(request):
#      if request.method == 'POST':
#         try:
#             # Get the product details from the POST request
#             product_name = request.POST.get('name')
#             product_price = Decimal(request.POST.get('price')) * 100  # Convert to cents for Stripe
#             product_description = request.POST.get('description')

#             user_email = request.user.email  

#             # Create a Stripe checkout session
#             checkout_session = stripe.checkout.Session.create(
#                 line_items=[
#                     {
#                         'price_data': {
#                             'currency': 'usd',
#                             'unit_amount': int(product_price),  # Stripe requires the price in cents
#                             'product_data': {
#                                 'name': product_name,
#                                 'description': product_description,
#                                 'images': ['https://images.unsplash.com/photo-1579202673506-ca3ce28943ef'],
#                             },
#                         },
#                         'quantity': 1,
#                     },
#                 ],
#                 mode='payment',
#                 billing_address_collection='required',
#                 success_url=DOMAIN + '/success',
#                 cancel_url=DOMAIN + '/cancel',
#                 customer_email=user_email,
#             )
            
#             return redirect(checkout_session.url)
#         except Exception as error:
#             return render(request, 'public/error.html', {'error': error})

#      return render(request, 'public/cancel.html')


# def success(request):
#     return render(request,'success.html')

# def cancel(request):
#     return render(request,'cancel.html')





# def create_checkout_session(request):
#     if request.method == 'POST':
#         try:
#             productId = request.POST.get('productId')
         
#             user_email = request.user.email    
#             checkout_session = stripe.checkout.Session.create(

#                 line_items=[
#                     {
#                         'price': productId ,
#                         'quantity': 1,
#                     },
#                 ],
#                 mode='subscription',
#                 billing_address_collection='required',
#                 success_url=DOMAIN + '/success',
#                 cancel_url=DOMAIN + '/cancel',
#                 customer_email=user_email,
#                 metadata={
#                 'plan_id': productId,
#                 }
#             )
            
#             return redirect(checkout_session.url)
#         except Exception as error:
          
#             return render (request,'public/error.html',{'error':error})

#     return render(request, 'public/cancel.html')




# @csrf_exempt 
# def stripe_webhook(request):
  
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     endpoint_secret = settings.WEBHOOK_ENDPOINT_SECRET
    
#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#     except ValueError:
#         return HttpResponse(status=400)
    
#     except stripe.error.SignatureVerificationError :
#         return HttpResponse(status=400)

   
#     if event['type'] == 'checkout.session.completed' :
#         print(event)
#         print('Payment was successful.') 
      

    
#     return HttpResponse(status=200)
#----------------------------------------------------------------------------------------------------------------

def addtocart(request,id):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        quantity = request.POST.get('quantity')
        total = request.POST.get('total')
        # print(total)
        # print(quantity)
        data = Cart(usercart = Register.objects.get(id=user_id),userpro = Products.objects.get(id=id),quantity = quantity,total = total)
        data.save()
        product = data.userpro
        if product.product_stock > 0:  # Ensure stock is available
            product.product_stock -= int(quantity)
            product.save()
        return redirect('cart')
    
def removepro(request,id):
    data = Cart.objects.filter(id=id).delete()
    return redirect('cart')
def checkoutdata(request):
    if request.method == "POST":
        checkoutid = request.session.get('user_id')
        adress = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        data = Cart.objects.filter(usercart = checkoutid,status = 0)

        for i in data:
            data = Checkout(usercheckout = Register.objects.get(id = checkoutid), usercart = Cart.objects.get(id=i.id),adress = adress,city = state, pincode = pincode, country = country)
            data.save()
            Cart.objects.filter(id=i.id).update(status=1)
        return redirect('create_payment')
def sucess(request):
    if 'user_id' in request.session:
       user_id = request.session.get('user_id')
       data = Checkout.objects.filter(usercheckout = user_id)
       return render(request,'sucess.html',{'data':data})
    return render(request,'login.html',{'msg1':"You want to Login"})


def viewcatpro(request,category):
    if 'user_id' in request.session:
       category_name = Category.objects.filter(category_name = category)
       data = Products.objects.filter(product_category = category)
       return render(request,'singlecat.html',{'data':data,'category_name':category_name})
    return render(request,'login.html',{'msg1':"You want to Login"})

def profile(request):
    if 'user_id' in request.session:
       user_id = request.session.get('user_id')
       data = Register.objects.get(id = user_id)
       return render(request,'profile.html',{'data':data})
    return render(request,'login.html',{'msg1':"You want to Login"})

def editprofile(request):
    if 'user_id' in request.session:
       user_id = request.session.get('user_id')
       data = Register.objects.get(id = user_id)
       return render(request,'editprofile.html',{'data':data})
    return render(request,'login.html',{'msg1':"You want to Login"})

def updateprofile(request):
        if request.method == "POST":
            user_id = request.session.get('user_id')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            place = request.POST.get('place')
            Register.objects.filter(id = user_id).update(name = name,email = email,phone = phone,place = place)
            return redirect('profile')






