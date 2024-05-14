from django.shortcuts import render,redirect
from product.models import ProductTable
# Create your views here.

def add_product(request):
    
     if request.method=="POST":
        name=request.POST.get("name")
        price=request.POST.get("price")
        description=request.POST.get("description")
        quantity=request.POST.get("quantity")
        category=request.POST.get("category")
        image=request.FILES.get("image")
        is_available=(request.POST.get('is_available',False)) and ('is_available' in request.POST)
        product=ProductTable.objects.create(name=name,price=price,description=description,quantity=quantity,category=category,image=image,is_available=is_available)
        
        
        product.save()
        return redirect("/admin/product/show/")
     return render(request,"admin/product/add_product.html")

def show_product(request):
    data={}
    all_product=ProductTable.objects.all()
    print(all_product.count())
    data["products"]=all_product
    return render(request,"admin/product/show_product.html",context=data)

def delete_product(request,id):
    product=ProductTable.objects.get(id=id)
    product.delete()
    return redirect("/admin/product/show/")

def update_product(request,id):
    data={}
    product=ProductTable.objects.get(id=id)
    print(product.name)
    data["product"]=product
    if request.method=="POST":
        product.name=request.POST.get("name")
        product.price=request.POST.get("price")
        product.description=request.POST.get("description")
        product.quantity=request.POST.get("quantity")
        product.category=request.POST.get("category")
        # image=request.FILES.get("image")
        # # is_available=(request.POST.get('is_available',False)) and ('is_available' in request.POST)
        # product=ProductTable.objects.filter(pk=id)
        # product.update(name=name,price=price,description=description,quantity=quantity,category=category,image=image,is_available=is_available)
        if request.FILES["image"]:
            product.image=request.FILES["image"]
            product.save()
    
        return redirect("/admin/product/show/")
    return render(request,"admin/product/update_product.html",context=data)



