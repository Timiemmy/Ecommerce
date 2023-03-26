from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.itembrowse, name='itembrowse'),
    path('<int:pk>/', views.detail, name='detail'),
    path('newitem/', views.newitem, name="newitem"),
    path('<int:pk>/delete/', views.deleteitem, name='delete'),
    path('<int:pk>/edit', views.edititem, name='edit')
]
