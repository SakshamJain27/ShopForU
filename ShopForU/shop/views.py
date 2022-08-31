from django.shortcuts import render
from math import ceil
from .models import Product, Orders, Track
from django.http import HttpResponse
import json

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'index.html', params)

def about(request):
    return render(request, 'about.html')

def contact(request):
    pass

def track(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = Track.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'Tracker.html')


def searchMatch(query, item):
    if query in item.product_name or query in item.category:
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'search.html', params)

def viewpro(request, id):
    product = Product.objects.filter(id=id)
    print(product)
    return render(request, 'view.html', {'product':product[0]})

def checkout(request):
    if request.method == "POST":
            items_json = request.POST.get('itemsJson', '')
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            amount = request.POST.get('amount', '')
            address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            phone = request.POST.get('phone', '')
            order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                           state=state, zip_code=zip_code, phone=phone, amount=amount)
            order.save()
            update = Track(order_id=order.order_id, update_desc="Your order has been placed")
            update.save()
            thank = True
            id = order.order_id
            return render(request, 'checkout.html', {'thank': thank, 'id': id})
    return render(request, 'checkout.html')
