from django.shortcuts import render
from rest_framework import generics 
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status 
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework_csv.renderers import CSVRenderer
from rest_framework_yaml.renderers import YAMLRenderer
# Create your views here.
class MenuItemsView(generics.ListCreateAPIView):
  queryset = MenuItem.objects.all()
  serializer_class = MenuItemSerializer

class SingleItemItemView(generics.RetrieveAPIView, generics.DestroyAPIView):
  queryset = MenuItem.objects.all()
  serializer_class = MenuItemSerializer


@api_view(['GET', 'POST'])
def menu_items(request):
  if request.method == 'GET':
    items = MenuItem.objects.select_related('category').all()
    serializer_items = MenuItemSerializer(items, many = True, context={'request': request})
    return Response(serializer_items.data)
  elif request.method == 'POST':
    serializer_item = MenuItemSerializer(data=request.data)
    serializer_item.is_valid(raise_exception=True)
    serializer_item.save()
    return Response(serializer_item.data, status = status.HTTP_201_CREATED)

@api_view()
def single_item(request, pk):
  item = get_object_or_404(MenuItem, pk=pk)
  serializer_item = MenuItemSerializer(item)
  return Response(serializer_item.data)

@api_view()
def category_detail(request, pk):
  category = get_object_or_404(Category, pk=pk)
  serialized_category = CategorySerializer(category)
  return Response(serialized_category.data)


@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
  items = MenuItem.objects.select_related('category').all()
  serialized_item = MenuItemSerializer(items, many=True)
  return Response({'data':serialized_item.data}, template_name='menu-items.html')

@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
  data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
  return Response(data)

