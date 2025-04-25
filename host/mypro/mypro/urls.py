"""
URL configuration for mypro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('about',views.about),
    path('blog',views.blog),
    path('service',views.service),
    path('contact',views.contact),
    path('registration',views.registration),
    path('login',views.login),
    path('adminindex',views.adminindex),
    path('userindex',views.userindex),
    path('add',views.add),
    path('category',views.addcategory),
    path('manage',views.manage),
    path('orderss',views.orderss),
    path('Enquiry',views.Enquiry),
    path('logout',views.logout),
    path('profile',views.profile),
    path('products',views.products),
    path('cart',views.cartdisplay),
    path('wishlist',views.wish_list),
    path('wishlistadd/<int:i>', views.wishlistadd),
    path('trash/<int:i>',views.trash),
    path('remove/<int:i>',views.remove),
    path('cartadd/<int:i>',views.cartadd),
    path('quantity/<int:i>', views.quantity),
    path('quan_tity/<int:i>', views.quan_tity),
    path('my order',views.my_order),
    path('delete/<int:i>', views.delete),
    path('update/<int:i>', views.update),
    path('payment/<int:i>',views.payment),
    path('success',views.success),
    path('logout',views.logout),
    path('edit_profile',views.edit_profile),
    path('productstatus/<int:i>',views.productstatus),
    path('forgot', views.forgot_password),
    path('reset_password/<token>', views.reset_password),









]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)