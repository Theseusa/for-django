from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$',index_views),
    url(r'^login/$',login_views,name='login'),
    url(r'^register/$',register_views,name='reg'),
    url(r'check_uphone/$',check_uphone_views),
    url(r'^check_login',check_login_views),
    url(r'^logout/$',logout_views),
    url(r'^load_type_goods/$',type_goods_views),
    url(r'^add_cart/$',add_cart_views),
]