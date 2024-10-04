"""backend URL Configuration

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
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index.html', views.index),
    path('about.html', views.about),
    path('login.html', views.login),
    path('masterpiece-detail.html', views.masterpiece_detail),
    path('masterpiece.html', views.masterpiece),   
    path('member.html', views.member),
    path('register-quiz.html', views.register_quiz),
    path('register.html', views.register),
    path('tutorial.html', views.tutorial),
    path('tutorial-detail.html', views.tutorial_detail),
    path('person.html', views.person)
]
