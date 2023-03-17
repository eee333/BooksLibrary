"""books_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from service.views import BookListView, BookDetailView, BookUpdateView, BookDeleteView, BookCreateView, AuthorViewSet, \
    CustomerCreateView, CustomerDeleteView, CustomerUpdateView, CustomerDetailView, CustomerListView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.SimpleRouter()
router.register('author', AuthorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('book/', BookListView.as_view()),
    path('book/<int:pk>/', BookDetailView.as_view()),
    path('book/update/<int:pk>/', BookUpdateView.as_view()),
    path('book/delete/<int:pk>/', BookDeleteView.as_view()),
    path('book/create/', BookCreateView.as_view()),
    path('customer/', CustomerListView.as_view()),
    path('customer/<int:pk>/', CustomerDetailView.as_view()),
    path('customer/update/<int:pk>/', CustomerUpdateView.as_view()),
    path('customer/delete/<int:pk>/', CustomerDeleteView.as_view()),
    path('customer/create/', CustomerCreateView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]

urlpatterns += router.urls
