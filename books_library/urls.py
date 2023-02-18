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

from service.views import AuthorListView, AuthorDetailView, AuthorUpdateView, AuthorDeleteView, AuthorCreateView, \
    BookViewSet, CustomerViewSet

router = routers.SimpleRouter()
router.register('book', BookViewSet)
router.register('customer', CustomerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('author/', AuthorListView.as_view()),
    path('author/<int:pk>', AuthorDetailView.as_view()),
    path('author/update/<int:pk>', AuthorUpdateView.as_view()),
    path('author/delete/<int:pk>', AuthorDeleteView.as_view()),
    path('author/create/', AuthorCreateView.as_view()),
]

urlpatterns += router.urls
