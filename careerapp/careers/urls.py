from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NguoiDungViewSet, NguoiTimViecViewSet, NhaTuyenDungViewSet, ViecLamViewSet, ViecLamDetailAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

router = DefaultRouter()
router.register(r'nguoi-dung', NguoiDungViewSet, basename='nguoi-dung')
router.register(r'nguoi-tim-viec', NguoiTimViecViewSet, basename='nguoi-tim-viec')
router.register(r'nha-tuyen-dung', NhaTuyenDungViewSet, basename='nha-tuyen-dung')
router.register(r'viec-lam', ViecLamViewSet, basename='viec-lam')
urlpatterns = [
    path('', include(router.urls)),
    path('viec-lam/<int:id>/', ViecLamDetailAPIView.as_view(), name='chi-tiet-viec-lam'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
