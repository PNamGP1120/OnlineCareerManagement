from django.urls import path, include
# accounts/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import (NguoiDungViewSet,
                    NguoiTimViecViewSet,
                    NhaTuyenDungViewSet,
                    ViecLamViewSet,
                    ViecLamDetailAPIView,
                    CVViewSet, YeuCauTuyenDungViewSet)
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


# Tạo đối tượng router
router = DefaultRouter()
router.register(r'nguoi-dung', NguoiDungViewSet, basename='nguoi-dung')
router.register(r'nguoi-tim-viec', NguoiTimViecViewSet, basename='nguoi-tim-viec')
router.register(r'nha-tuyen-dung', NhaTuyenDungViewSet, basename='nha-tuyen-dung')
router.register(r'viec-lam', ViecLamViewSet, basename='viec-lam')
router.register(r'cv', CVViewSet, basename='cv')
router.register(r'ung-tuyen', YeuCauTuyenDungViewSet, basename='yeucau')



# Cấu hình URL cho router
urlpatterns = [
    path('', include(router.urls)),
    path('viec-lam/<int:id>/', ViecLamDetailAPIView.as_view(), name='chi-tiet-viec-lam'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
