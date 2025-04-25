import datetime

from django.shortcuts import render,redirect
from django.http import HttpResponse

import razorpay
from django.contrib import messages
from .forms import *
from django.utils.crypto import get_random_string # type: ignore
from django.core.mail import send_mail # type: ignore



# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request,'about-us.html')
def blog(request):
    return render(request,'blog.html')
def contact(request):
    if request.method == 'POST':
        a = request.POST['Name']
        b = int(request.POST['phoneNumber'])
        c = request.POST['Email']
        d = request.POST['messagebox']
        contacts.objects.create(name=a, phone=b, email=c, messagebox=d,).save()
    return render(request,'contacts.html')
def service(request):
    return render(request,'services.html')
from .models import *
def registration(request):
    print("firu")
    if request.method == 'POST':
        print("hello")
        a = request.POST['Name']
        b = int(request.POST['phoneNumber'])
        c = request.POST['Email']
        d = request.POST['username']
        e = request.POST['password']
        f = request.POST['confirmpassword']
        if user_resgister.objects.filter(username=d).exists():
            messages.error(request,'Username already exist')
            return redirect(registration)
        if user_resgister.objects.filter(email=c).exists():
            messages.error(request, 'Email already exist')
            return redirect(registration)
        else:
            if e==f:
                user_resgister.objects.create(name=a, phone=b, email=c, username=d, password=e).save()
                messages.success(request, 'Register successfully')
                return redirect(registration)
            else:
                messages.error(request, 'Password Doesnot match')
                return redirect(registration)

    return render(request,'registration.html')

def login(request):
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['password']
        try:
            data = user_resgister.objects.get(username=a)
            if data.password == b:
                request.session['user'] = a
                return redirect(userindex)
            else:
                messages.error(request,'Invalid Password')
                return redirect(login)
        except Exception as e:
            print(e)
            if a=='admin' and b=='admin123':
                 request.session['admin'] = a
                 return redirect(adminindex)
            else:
                 messages.error(request, 'Invalid Email or password')
                 return redirect(login)
    else:
        return render(request,'login.html')
def adminindex(request):
    if 'admin' in request.session:
        return render(request, 'adminindex.html')
    else:
        return redirect(login)
def userindex(request):
    if 'user' in request.session:
        return render(request,'userindex.html')
    else:
        return redirect(login)
def add(request):
    if 'admin' in request.session:
        data=category.objects.all()
        if  request.method == 'POST':
            a=  request.POST['Name']
            b = request.POST['price']
            c = request.POST['quantity']
            d=  request.POST['category']
            e=  request.FILES['image']
            print(d)
            cat=category.objects.get(name=d)
            product.objects.create(name=a,price=b,quantity=c,category=cat,image=e).save()
            messages.success(request,'Product Added')
            return redirect(add)
        return render(request,'add.html',{'data':data})
    else:
        return redirect(login)


def addcategory(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a=request.POST['category_name']
            category.objects.create(name=a).save()
            messages.success(request,'Category added')
        return render(request,'category.html')
    else:
        return redirect(login)
def manage(request):
    if 'admin' in request.session:
        a = product.objects.all()
        return render(request,'manage.html',{'data':a})
    else:
        return redirect(login)
def orderss(request):
    data = myorder.objects.all()
    return render(request,'orderss.html',{'data':data})
def Enquiry(request):
    data = contacts.objects.all()
    return render(request,'Enquiry.html',{'data': data})
def logout(request):
    if 'user' in request.session or 'admin' in request.session:
        request.session.flush()
        return redirect(login)
    return redirect(login)


def profile(request):
    if 'user' in request.session:
        if request.method == 'GET':
            a=request.session['user']
            data=user_resgister.objects.get(username=a)
            return render(request,'profile.html',{'r':data})
        else:
            return render(request,'userindex.html')
    else:
        return redirect(login)


def edit_profile(request):
    if 'user' in request.session:
        a = request.session['user']
        data = user_resgister.objects.get(username=a)
        p = Profile(instance=data)
        print(p)
        if request.method=='POST':
            p=Profile(request.POST,instance=data)
            if p.is_valid():
                p.save()
                return redirect(profile)

        return render(request,'edit_profile.html',{'p':p})
    else:
        return redirect(login)

#     ---------------------------User Views ----------------------------------

def products(request):
    if 'user' in request.session:
        data = product.objects.all()
        return render(request,'products.html',{'data':data})
    else:
        return redirect(login)

def delete(request,i):
    if 'admin' in request.session:
        data=product.objects.get(pk=i)
        data.delete()
        messages.error(request,'Product Removed')
        return redirect(manage)
    else:
        return redirect(login)
def update(request,i):
    if 'admin' in request.session:
        data=product.objects.get(pk=i)
        f = modelform(instance=data)
        if request.method == 'POST':
             f = modelform(request.POST, request.FILES, instance=data)
             if f.is_valid():
                 f.save()
                 messages.success(request,'Updated successfully')
                 return redirect(manage)
             return redirect(manage)
        return render(request, 'update.html', {'data': data,'f':f})
    else:
        return redirect(login)
def cartdisplay(request):
    if 'user' in request.session:
        user = user_resgister.objects.get(username=request.session['user'])
        data = cart.objects.filter(user_details=user)
        total = 0
        quantity = 0

        for i in data:
            i.total_price = i.product_details.price
            i.total_price = i.product_details.price * i.quantity
            print(i.total_price)
            total += i.total_price
            quantity += 1
        return render(request, 'cart.html', {'data': data, 'total': total, 'quantity': quantity})
    else:
        return redirect(login)

def wish_list(request):
    if 'user' in request.session:
        user = user_resgister.objects.get(username=request.session['user'])
        data = wishlist.objects.filter(user_details=user)
        return render(request, 'wish.html', {'data': data})
    else:
        return redirect(login)

def cartadd(request,i):
    if 'user' in request.session:
        a = product.objects.get(pk=i)
        user = user_resgister.objects.get(username=request.session['user'])
        if cart.objects.filter(product_details=a).exists():
            data = cart.objects.get(product_details=a)
            data.quantity += 1
            data.save()
        else:
            cart.objects.create(product_details=a, user_details=user, total_price=a.price).save()
            messages.success(request,'cart added successfully')
            return redirect(products)
        return redirect(products)
    else:
        return redirect(login)

def wishlistadd(request,i):
    if 'user' in request.session:
        a = product.objects.get(pk=i)
        user = user_resgister.objects.get(username=request.session['user'])
        wishlist.objects.create(product_details=a, user_details=user).save()
        messages.success(request,'Added to Wishlist')
        return redirect(products)
    else:
        return redirect(login)

def trash(request,i):
    if 'user' in request.session:
        data=cart.objects.get(pk=i)
        data.delete()
        messages.error(request,'Removed from the cart')
        return redirect(cartdisplay)
    else:
        return redirect(login)

def remove(request,i):
    if 'user' in request.session:
        data=wishlist.objects.get(pk=i)
        data.delete()
        messages.error(request, 'Removed from the wishlist')
        return redirect(wish_list)
    else:
        return redirect(login)

def quantity(request,i):
    if 'user' in request.session:
        data =cart.objects.get(pk=i)
        data.quantity +=1
        data.total_price=data.quantity*data.product_details.price
        data.save()
        return redirect(cartdisplay)
    else:
        return redirect(login)
def quan_tity(request,i):
    if 'user' in request.session:
        data =cart.objects.get(pk=i)
        data.quantity -=1
        if data.quantity <1:
            data.delete()
        else:
         data.save()
        return redirect(cartdisplay)
    else:
        return redirect(login)

def payment(request, i):
    if 'user' in request.session:
        print(i)
        amount = i * 100
        request.session['amount']=amount
        order_currency = 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        # cursor = connection.cursor()
        # cursor.execute(
        #     "update inspection_details set status='completed', fine_paid_date = curdate() where insp_id='" + str(
        #         id) + "' ")

        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        return render(request, "payment.html", {'amount': amount})
    else:
        return redirect(login)

def success(request):
    if 'user' in request.session:
        print(request.session['amount'])
        user = user_resgister.objects.get(username=request.session['user'])
        data = cart.objects.filter(user_details=user)
        date=datetime.datetime.now()
        for i in data:
            myorder.objects.create(user_details=user,product_details=i.product_details,product_status='order confirmed', quantity=i.quantity, payment_amount=(request.session['amount']),order_date=date ).save()
            data.delete()
            return render(request, 'success.html',{'data': data})

    else:
        return redirect(login)

def my_order(request):
    if 'user' in request.session:
        user = user_resgister.objects.get(username=request.session['user'])
        data = myorder.objects.filter(user_details=user)

        return render(request, 'my order.html', {'data': data})

    else:
        return redirect(login)

def productstatus(request,i):
    data=myorder.objects.get(pk=i)
    if request.method == 'POST':
        a = request.POST['status']
        data.product_status=a
        data.save()
        messages.success(request,'order updated')
        return redirect(orderss)
    else:
        return redirect(orderss)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = user_resgister.objects.get(email=email)
        except:  # noqa: E722
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user_details=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset_password/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except Exception as e:  # noqa: E722
            print(e)
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request,'forgot.html')

def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user_details.password=new_password
            password_reset.user_details.save()
            messages.success(request,'Password Reset successfully')
            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html', {'token': token})


