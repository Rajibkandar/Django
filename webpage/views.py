from email import message
from math import ceil
from django.shortcuts import render,HttpResponse,redirect
from .models import product,Contact,Order,Orderupdate
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    allprods=[]
    catprods=product.objects.values('category', 'id')
    cats={item['category'] for item in catprods }
    for cat in cats:
        prod=product.objects.filter(category=cat)
        n=len(prod)
        nslides=n//4 +ceil((n/4)-(n//4))
        allprods.append([prod,range(1,nslides),nslides])
        params={'allprods':allprods}
    return render(request,'index.html',params)

    
def searchmatch(query,item):
    if query in item.product_description.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    elif query in item.product_description.upper() or query in item.product_name.upper() or query in item.category.upper():
        return True
    else:
        return False
def search(request):
    query=request.GET.get('search')
    allprods=[]
    catprods=product.objects.values('category', 'id')
    cats={item['category'] for item in catprods }
    for cat in cats:
        prodtemp=product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchmatch(query,item)]
        n=len(prod)
        nslides=n//4 +ceil((n/4)-(n//4))
        if len(prod)!=0:
            allprods.append([prod,range(1,nslides),nslides])
        params={'allprods':allprods}
    if len(allprods)==0 or len(query)<3:
        params={'msg':" please make sure you enter relevant search query"}
    return render(request,'search.html',params)

def productpage(request,myid):
    products=product.objects.filter(id=myid)
    return render(request,'product.html',{'product':products[0]})

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        if len(name)<3 or len(email)<3 :
            messages.error(request,"please fill the form correctly")
        if len(desc)<20:
            messages.error(request,"your quesry must be more than 20 words")
        else:
            contact=Contact(name=name,email=email,phone=phone,desc=desc)
            contact.save()
            messages.success(request,"your problem  has been submitted and our team will contact you")
    return render(request,'contact.html')
def checkoutpage(request):
    if request.method=="POST":
        item_json=request.POST.get('itemsJson','')
        name=request.POST.get('name','')
        amount=request.POST.get('amount','')
        email=request.POST.get('email','')
        address=request.POST.get('address','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        persnalcart=request.POST.get('persnalcart','')
        integerpersnalcart=int(persnalcart)
        if len(name)<3:
            print(name)
            messages.error(request,"please name must be frester than 3 words")
        elif len(address)<10:
            messages.error(request,"please enter a valid address")
        elif len(city)<3:
            messages.error(request,"please enter your city correctly")
        elif len(state)<3:
            messages.error(request,"please enter your state correctly")
        elif len(zip_code)<5 or len(zip_code)>10:
            messages.error(request,"enter valid zip code")
        elif len(phone)<10 or len(phone)>10:
            messages.error(request,"enter valid phone number")
        elif integerpersnalcart<1:
            messages.error(request,"your cart is empty")
        else:
            order=Order(item_json=item_json,name=name,amount=amount,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
            order.save()
            update=Orderupdate(order_id=order.order_id,update_desc="the order has been placed")
            update.save()
            thank=True
            id=order.order_id
            return render(request,'checkoutpage.html',{'thank':thank,'id':id})
        
    return render(request,'checkoutpage.html')
def tracker(request):
    if request.method=="POST":
        orderId=request.POST.get('orderId','')
        email=request.POST.get('email','')
        try:
            order=Order.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update=Orderupdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps({"status":"success","updates":updates,"itemsJson":order[0].item_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request,'tracker.html')
def handlesignup(request):
    if request.method=='POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['signupemail']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if len(username)<3:
            messages.error(request,"username must be greater")
            return redirect('/')
        if not username.isalnum():
            messages.error(request,"username should only contain string and number")
        if password1!=password2:
            messages.error(request,"password do not match")
            return redirect('/')

        myuser=User.objects.create_user(username,email,password1)
        myuser.first_name=firstname
        myuser.last_name=lastname
        myuser.save()
        messages.success(request,"your account is created")
        return redirect('/')

    else:
        return HttpResponse('page not found')
def handlelogin(request):
    if request.method=='POST':
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"successfully login")
            return redirect('/')
    return HttpResponse("handle login")
def handlelogout(request):
    logout(request)
    messages.success(request,"successfully logout")
    return redirect('/')