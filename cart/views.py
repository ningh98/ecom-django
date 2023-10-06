
from django.views import generic
# Create your views here.

from .models import Product

class ProductListView(generic.ListView):
    template_name = 'cart/product_list.html'
    queryset = Product.objects.all()