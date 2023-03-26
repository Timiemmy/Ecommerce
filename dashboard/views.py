from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from items.models import Item


@login_required
def dashboard(request):
    items = Item.objects.filter(seller=request.user)

    return render(request, 'dashboard/index.html', {'items': items})
