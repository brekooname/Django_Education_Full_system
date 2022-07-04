"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views, user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE,name='base'),
    path('', views.HOME,name='home'),
    path('contact-us/', views.CONTACT_US,name='contact-us'),
    path('about-us/', views.ABOUT_US,name='about-us'),
    path('courses/', views.COURSES,name='courses'),
    path('courses/<slug>', views.COURSE_DETAIL,name='course_detail'),
    path('mycourse/', views.MYCOURSE,name='mycourse'),
    path('search/', views.SEARCH,name='search'),
    path('fillter-data/', views.FILLTER_DATA,name='fillter_data'),
    path('course/fillter-data', views.FILLTER_DATA_ALL,name='fillter_data_all'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/register/',user_login.REGISTER,name='register'),
    path('accounts/profile/',user_login.PROFILE,name='profile'),
    path('accounts/profile/update',user_login.PROFILE_UPDATE,name='profile_update'),
    path('accounts/image/upload',user_login.IMAGE_UPLOAD,name='image_upload'),
    path('dologin',user_login.LOGIN,name='dologin'),
    path('logout/',user_login.LOGOUT,name='logout'),
    path('error', views.ERROR,name='404'),
    path('checkout/<slug>',views.CHECKOUT,name='checkout'),
    path('verify_payment',views.VERIFY_PAYMENT,name='verify_payment'),
    path('review/<slug>',views.REVIEW,name='review'),
    path('author/profile/<id>',views.AUTHOR_PROFILE,name='author_profile'),
    path('blog/<slug>',views.BLOG_DETAIL,name='blog_detail')

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
