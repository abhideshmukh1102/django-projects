from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from product.models import ProductTable,CartTable
from django.db.models import Q
from django.contrib import messages
# from django.contrib.auth.decorators import login_required

# Create your views here.







def register_user(request):
   data={}
   
   if request.user.is_authenticated:
      if request.user.is_superuser:
         return redirect("/admin")
      else:
         return redirect("/")
      
   
   
   if request.method=="POST":
      uname=request.POST["username"]
      upass=request.POST["password"]
      uconfpass=request.POST["password2"]
      
      if(uname=="" or upass=="" or uconfpass==""):
         data["error_msg"]=" Field cant be empty"
         return render(request,"user/register.html",context=data)
      
      elif(upass!=uconfpass):
         data["error_msg"]=" password and confirm password does not matched"
         return render(request,"user/register.html",context=data)
      
      elif(User.objects.filter(username=uname).exists()):
         data["error_msg"]=uname + " already exist"
         return render(request,"user/register.html",context=data)
      
      else:
         user=User.objects.create(username=uname)
         user.set_password(upass)
         user.save()
         return redirect(" /login")
   return render(request,"user/register.html")


def login_user(request):
   data={}
   
   if request.user.is_authenticated:
      if request.user.is_superuser:
         return redirect("/admin")
      else:
         return redirect("/")
         
      
    
   if request.method=="POST":
      uname=request.POST["username"]
      upass=request.POST["password"]
      
      if(uname=="" or upass==""):
         data["error_msg"]=" Field cant be empty"
         return render(request,"user/login.html",context=data)
      
      elif(not User.objects.filter(username=uname).exists()):
         data["error_msg"]=uname + " is not registered"
         return render(request,"user/login.html",context=data)
      
      else:
         user=authenticate(username=uname,password=upass)
         print(user)
         if user is not None:
            login(request,user)
            if user.is_superuser:
               return redirect("/admin")
            
            else:
               return redirect("/")
               
         else:
            data["error_msg"]= "wrong password"
            return render(request,"user/login.html",context=data)
   return render(request,'user/login.html')



# def home(request):
#    data={}
#    user_authenticated=request.user.is_authenticated
#    print(user_authenticated)
#    if(user_authenticated):
#       user_id=request.user.id
#       user=User.objects.get(id=user_id)
#       data["user_data"]=user.username
#       return render(request,"base.html",context=data)
   
#    else:
#       data["user_data"]="unkonwn user"
#       return render(request,"base.html",context=data)
         
#    return render(request,"base.html")



def logout_user(request):
   logout(request)
   return redirect("/")


def admin_panel(request):
   if not request.user.is_superuser:
      return redirect("/")
   return render(request,"admin/admin.html")
 
# --------------------------------------------logic on user dashboard-------------------------
global_product=ProductTable.objects.none()
def home(request):
   data={}
   global global_product
   global filtered_product
   global_product=ProductTable.objects.filter(is_available=True)
   filtered_product=global_product
   data["products"]=global_product
   
   
   user_id=request.user.id
   cart=CartTable.objects.filter(uid=user_id)
   data["cartvalue"]=cart.count()
   return render(request,"base.html",context=data)


def filter_by_category(request,category_value):
   data={}
   q1=Q(is_available=True)
   q2=Q(category=category_value)
   global global_product
   global filtered_product
   filtered_product=global_product.filter(q1 & q2)
   data["products"]=filtered_product
   return render(request,"base.html",context=data)


def sort_by_price(request,sort_value):
   data={}
   global filtered_product
   if(sort_value=="asc"):
      sorted_product=filtered_product.filter(is_available=True).order_by("price")
   else:
      sorted_product=filtered_product.filter(is_available=True).order_by("-price")
      
      
   data["products"]=sorted_product
   return render(request,"base.html",context=data)


def search_price_range(request):
   print('hello boss')
   data={}
   min=request.POST["min"]
   max=request.POST["max"]
   q1=Q(is_available=True)
   q2=Q(price__gte=min)
   q3=Q(price__lte=max)
   searched_product=filtered_product.filter(q1 & q2 & q3)
   data["products"]=searched_product
   return render(request,"base.html",context=data)

def add_to_cart(request,product_id):
   if request.user.is_authenticated:
      user=request.user
      product=ProductTable.objects.get(id=product_id)
      q1=Q(uid=request.user.id)
      q2=Q(pid=product_id)
      cart_value=CartTable.objects.filter(q1 & q2)
      if(cart_value.count()>0):
         messages.error(request,"Product is already in the cart")
      else:
         cart=CartTable.objects.create(uid=user,pid=product,quantity=1)
         cart.save()
         messages.success(request,"Product is added to the cart")
      return redirect("/")
   else:
      return redirect("/login")
   
   
def find_cart_value(request):
   user_id=request.user.id
   cart=CartTable.objects.filter(uid=user_id)
   cart_count=cart.count()
   return cart_count

def show_cart(request):
   data={}
   total_item=0
   total_price=0
   cart_count=find_cart_value(request)
   data["cartvalue"]=cart_count
   product_in_cart=CartTable.objects.filter(uid=request.user.id)
   data["cartproducts"]=product_in_cart
   for product in product_in_cart:
      total_item+=product.quantity
      total_price+=(product.pid.price*product.quantity)
   data["total_item"]=total_item
   data["total_price"]=total_price
   return render(request,"home/show_cart.html",context=data)
   
def delete_cart(request,cart_id):
   cart=CartTable.objects.get(id=cart_id)
   cart.delete()
   return redirect("/cart")   

   
         
def update_cart_quantity(request,flag,cart_id):
   cart=CartTable.objects.filter(id=cart_id)
   actual_quantity=cart[0].quantity
   if flag=="inc":
      cart.update(quantity=actual_quantity+1)
   else:
      if(cart[0].quantity==1):
         pass
      else:
         cart.update(quantity=actual_quantity-1)
   return redirect("/cart")        

def show_order(request):
   data={}
   total_item=0
   total_price=0
   cart_count=find_cart_value(request)
   data["cartvalue"]=cart_count
   product_in_cart=CartTable.objects.filter(uid=request.user.id)
   data["cartproducts"]=product_in_cart
   for product in product_in_cart:
      total_item+=product.quantity
      total_price+=(product.pid.price*product.quantity)
   data["total_item"]=total_item
   data["total_price"]=total_price
   return render(request,"home/show_order.html",context=data)

import razorpay
def make_payment(request):
   
   total_price=0
   product_in_cart=CartTable.objects.filter(uid=request.user.id)
   for product in product_in_cart:
      total_price+=(product.pid.price*product.quantity)  
   client = razorpay.Client(auth=("rzp_test_KOj49wnPR6EjnV", "2fiaqoup3ixyWGnSc3OCCRhQ"))
   data = { "amount":int(total_price*100), "currency": "INR", "receipt": "order_rcptid_11" }
   payment = client.order.create(data=data)
   print(payment)
   return render(request,"home/pay.html",context=data)
   
