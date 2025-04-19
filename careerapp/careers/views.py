from pickle import FALSE

from rest_framework import viewsets, status, permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from .models import NguoiDung, NguoiTimViec, NhaTuyenDung, ViecLam
from .serializers import NguoiDungSerializer, NguoiTimViecSerializer, NhaTuyenDungSerializer, ViecLamSerializer
from .permissions import IsAdminOrReadOnly, IsNguoiTimViec, IsNhaTuyenDung

class NguoiDungViewSet(viewsets.ModelViewSet):
    queryset = NguoiDung.objects.filter(is_active =True).all()
    serializer_class = NguoiDungSerializer
    parser_classes = [MultiPartParser]

    # Áp dụng quyền hạn tùy chỉnh cho các hành động
    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]  # Cho phép tất cả người dùng tạo tài khoản
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]  # Chỉ admin có thể chỉnh sửa và xóa
        return [permissions.IsAdminUser()]  # Admin đã đăng nhập có thể xem

    def perform_create(self, serializer):
        # Tạo tài khoản cho người dùng mới
        user = serializer.save()
        # Không gán quyền gì thêm cho người dùng, mặc định không phải admin

    @action(detail=False, methods=['get'], url_path='nguoi_dung_hien_tai', url_name='nguoi_dung_hien_tai', permission_classes=[permissions.IsAuthenticated])
    def nguoi_dung_hien_tai(self, request):
        user = self.request.user
        return Response(NguoiDungSerializer(user).data)
    #
    # @action(detail=False, methods=['post'])
    # def register(self, request):
    #     """
    #     Đăng ký người dùng mới.
    #     """
    #     username = request.data.get('username')
    #     email = request.data.get('email')
    #     password = request.data.get('password')
    #     first_name = request.data.get('first_name', '')
    #     last_name = request.data.get('last_name', '')
    #     hinh_dai_dien = request.data.get('hinh_dai_dien')  # Trường hình ảnh từ Cloudinary
    #
    #     if not username or not email or not password:
    #         return Response(
    #             {"detail": "Username, email, and password are required."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #
    #     if NguoiDung.objects.filter(username=username).exists():
    #         return Response(
    #             {"detail": "Username is already taken."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #
    #     # Mã hóa mật khẩu
    #     user = NguoiDung(
    #         username=username,
    #         email=email,
    #         first_name=first_name,
    #         last_name=last_name,
    #         password=make_password(password)  # Mã hóa mật khẩu
    #     )
    #
    #     if hinh_dai_dien:
    #         user.hinh_dai_dien = hinh_dai_dien  # Lưu URL ảnh từ Cloudinary vào trường hinh_dai_dien
    #
    #     # Lưu người dùng vào cơ sở dữ liệu
    #     user.save()
    #
    #     # Trả về thông tin người dùng sau khi đăng ký thành công, bao gồm URL ảnh Cloudinary đầy đủ
    #     cloudinary_url = f"https://res.cloudinary.com/your_cloud_name/{user.hinh_dai_dien}" if user.hinh_dai_dien else None
    #
    #     return Response(
    #         {
    #             "username": user.username,
    #             "email": user.email,
    #             "first_name": user.first_name,
    #             "last_name": user.last_name,
    #             "hinh_dai_dien": cloudinary_url  # Trả về URL đầy đủ
    #         },
    #         status=status.HTTP_201_CREATED
    #     )

class NguoiTimViecViewSet(viewsets.ModelViewSet):
    queryset = NguoiTimViec.objects.all()
    serializer_class = NguoiTimViecSerializer
    permission_classes = [permissions.IsAuthenticated, IsNguoiTimViec]  # Chỉ người tìm việc mới có thể chỉnh sửa thông tin của mình

    def get_permissions(self):
        # Người tìm việc chỉ có thể xem và chỉnh sửa thông tin của chính họ
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsNguoiTimViec()]
        # Admin có thể xem tất cả
        elif self.action == 'list':
            return [permissions.IsAdminUser()]
        return super().get_permissions()  # Các hành động khác, bao gồm tạo mới, cho phép người dùng đã đăng nhập

class NhaTuyenDungViewSet(viewsets.ModelViewSet):
    queryset = NhaTuyenDung.objects.all()
    serializer_class = NhaTuyenDungSerializer
    permission_classes = [permissions.IsAuthenticated, IsNhaTuyenDung]  # Chỉ nhà tuyển dụng mới có thể chỉnh sửa thông tin của mình

    def get_permissions(self):
        # Nhà tuyển dụng có thể chỉnh sửa thông tin công ty của mình
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsNhaTuyenDung()]
        # Admin có thể xem tất cả
        elif self.action == 'list':
            return [permissions.IsAdminUser()]
        return super().get_permissions()  # Các hành động khác, bao gồm tạo mới, cho phép người dùng đã đăng nhập


class ViecLamViewSet(viewsets.ModelViewSet):
    queryset = ViecLam.objects.filter(is_active =True).all()
    serializer_class = ViecLamSerializer
    permission_classes = [permissions.AllowAny]


class ViecLamDetailAPIView(RetrieveAPIView):
    queryset = ViecLam.objects.filter(is_active=True)
    serializer_class = ViecLamSerializer
    lookup_field = 'id'