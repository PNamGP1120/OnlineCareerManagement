# accounts/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import NguoiDungViewSet, NguoiTimViecViewSet, NhaTuyenDungViewSet, dang_ky_nguoi_dung
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


# Tạo đối tượng router
router = DefaultRouter()

# Đăng ký các ViewSet vào router và thêm basename
router.register(r'nguoi_dung', NguoiDungViewSet, basename='nguoi_dung')
router.register(r'nguoi_tim_viec', NguoiTimViecViewSet, basename='nguoi_tim_viec')
router.register(r'nha_tuyen_dung', NhaTuyenDungViewSet, basename='nha_tuyen_dung')



# Cấu hình URL cho router
urlpatterns = [
    path('', include(router.urls)),  # Đảm bảo rằng bạn đã bao gồm URL từ router
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dang_ky_nguoi_dung/', dang_ky_nguoi_dung, name='dang_ky_nguoi_dung'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
