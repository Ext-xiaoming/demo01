"""demo01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from app1 import  views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('demotest/', views.demotest),  # 测试
    path('savePictures/',views.savePictures),
    path('postIfaceCheck/',views.postIfaceCheck),
    path('signUp/', views.signUp),
    path('login/', views.login),
    path('changePassward/', views.changePassward),
    path('numQiandaoS/', views.numQiandaoS),
    path('lodeTeaCourseList/', views.lodeTeaCourseList),
    path('lodeStuCourseList/', views.lodeStuCourseList),
    path('stuKaoQinList/', views.stuKaoQinList),
    path('whoQiandao/', views.whoQiandao),
    path('teaCourseFabu/', views.teaCourseFabu),
    path('teaPostCourse/', views.teaPostCourse),
    path('stuAddCourse/', views.stuAddCourse),
    path('teaPostNumCheck/', views.teaPostNumCheck),
    path('verIsCheck/', views.verIsCheck),

]
