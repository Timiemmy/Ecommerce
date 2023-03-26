from django.shortcuts import render
from items.models import Category, Item
# Create your views here.


def index(request):
    # This will filter objects that are not sold and displaly it
    # This will display only 6 products
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, "core/index.html", {
        'categories': categories,
        'items': items
    })


def contact(request):
    return render(request, "core/contact.html")
