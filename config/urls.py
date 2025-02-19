"""
URL configuration for config project.

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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from rest_framework.routers import DefaultRouter
from userSystem.views import *
from  kutuphane.views import (
    CategoryViewSet, PublisherViewSet, AuthorViewSet, BookViewSet,
    LoanViewSet, ReservationViewSet, CommentViewSet, FavoriteViewSet,
    PenaltyViewSet, BookTrackingViewSet
)

router=DefaultRouter()
router.register(r'user',UserViewSets,basename='userViewSet')
router.register(r'categories', CategoryViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'penalties', PenaltyViewSet)
router.register(r'booktrackings', BookTrackingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path('api/token/',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('api/token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('api/token/verify/',TokenVerifyView.as_view(),name="token_verify"),

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

