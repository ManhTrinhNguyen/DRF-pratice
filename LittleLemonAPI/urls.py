from . import views 
from django.urls import path 

urlpatterns = [
  path('menu-items', views.menu_items),
  path('menu-items/<int:pk>', views.single_item),
  path('menu', views.menu),
  path('category/<int:pk>',views.category_detail, name='category-detail'),
  path('welcome/', views.welcome)
]