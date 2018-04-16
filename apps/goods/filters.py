import django_filters
from .models import Goods,GoodsCategory
from django.db.models import Q
class GoodsFilter(django_filters.rest_framework.FilterSet):

    '''
    商品的过滤类
    '''
    price_min = django_filters.NumberFilter(name='shop_price',lookup_expr='gte',label='最低价格',help_text='最低价格')
    price_max = django_filters.NumberFilter(name='shop_price', lookup_expr='lte',label='最高价格',help_text='最高价格')
    # name = django_filters.CharFilter(name='name',lookup_expr='icontains')
    top_category = django_filters.NumberFilter(method='top_category_filter',label='该分类的所有子类',help_text='提供父类id，将给出所有子类')
    # def top_category_filter(self,name,queryset,value):#这是一个错误示范，注意参数的顺序
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value)|Q(category__parent_category=value)
                                   |Q(category__parent_category__parent_category=value))
    class Meta:
        model = Goods
        fields = ['is_hot','is_new']
        # fields = ['price_min', 'price_max', 'name']
