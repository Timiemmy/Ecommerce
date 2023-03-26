from django.shortcuts import render, get_object_or_404


from .models import Item
# Create your views here.


def detail(request, pk):
    items = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(  # This related items will filter it by items in thesame category and exclude the particular item showing only 3
        category=items.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, "item/detail.html", {'items': items, 'related_items': related_items})
