from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import NewItemForm, EditItemForm
from .models import Item, Category
# Create your views here.


def itembrowse(request):
    query = request.GET.get('query', '')
    items = Item.objects.filter(is_sold=False)
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) |
                             Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })


def detail(request, pk):
    items = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(  # This related items will filter it by items in thesame category and exclude the particular item showing only 3
        category=items.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, "item/detail.html", {'items': items, 'related_items': related_items})


@login_required
def newitem(request):
    if request.method == 'POST':
        # To get thr form and file uploaded
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user

            return redirect("item:detail", pk=item.id)
    else:
        form = NewItemForm()
    return render(request, 'item/new_item.html', {'form': form, 'title': 'Add Item'})


@login_required
def deleteitem(request, pk):
    # This will get the object if the seller is the owner.
    item = get_object_or_404(Item, pk=pk, seller=request.user)
    item.delete()  # this will delete it

    return redirect(request, 'dashboard:dashboard', {'item': item})


@login_required
def edititem(request, pk):
    item = get_object_or_404(Item, pk=pk, seller=request.user)
    if request.method == 'POST':
        # To get thr form and file uploaded
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect("item:detail", pk=item.id)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'item/new_item.html', {'form': form, 'title': 'Edit item'})
