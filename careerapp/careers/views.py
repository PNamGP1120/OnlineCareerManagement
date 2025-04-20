from pickle import FALSE

from rest_framework import viewsets, status, permissions, mixins, generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

from .models import NguoiDung, NguoiTimViec, NhaTuyenDung, ViecLam, CV, YeuCauTuyenDung
from .serializers import (NguoiDungSerializer,
                          NguoiTimViecSerializer,
                          NhaTuyenDungSerializer,
                          ViecLamSerializer,
                          CVSerializer, YeuCauTuyenDungSerializer)
from .permissions import (IsAdminOrReadOnly,
                          IsNguoiTimViec,
                          IsNhaTuyenDung,
                          IsOwnerOrAdmin, IsNguoiTimViecTaoYeuCauTuyenDung, IsNguoiTimViecXemYeuCauTuyenDung,
                          IsNhaTuyenDungXemVaChamKetQua)

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
    # permission_classes = [permissions.IsAuthenticated, IsNguoiTimViec]  # Chỉ người tìm việc mới có thể chỉnh sửa thông tin của mình

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
    # permission_classes = [permissions.IsAuthenticated, IsNhaTuyenDung]  # Chỉ nhà tuyển dụng mới có thể chỉnh sửa thông tin của mình

    def get_permissions(self):
        # Nhà tuyển dụng có thể chỉnh sửa thông tin công ty của mình
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsNhaTuyenDung()]
        # Admin có thể xem tất cả
        elif self.action == 'list':
            return [permissions.IsAdminUser()]
        return super().get_permissions()  # Các hành động khác, bao gồm tạo mới, cho phép người dùng đã đăng nhập


class ViecLamViewSet(viewsets.ModelViewSet):
    serializer_class = ViecLamSerializer

    def get_queryset(self):
        if self.request:
            if self.request.user.is_staff:
                return ViecLam.objects.all()
        return ViecLam.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if self.request.user.is_staff:
                return [permissions.IsAdminUser()]
            return [permissions.IsAuthenticated(), (IsNhaTuyenDung | permissions.IsAdminUser)()]
        return [permissions.AllowAny()]


class ViecLamDetailAPIView(RetrieveAPIView):
    serializer_class = ViecLamSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ViecLam.objects.all()
        return ViecLam.objects.filter(is_active = True)

class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticated, IsNguoiTimViec | IsAdminOrReadOnly, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CV.objects.all()
        elif hasattr(self.request.user, 'nguoi_tim_viec'):
            return CV.objects.filter(nguoi_tim_viec=self.request.user.nguoi_tim_viec)
        return CV.objects.none()

class YeuCauTuyenDungViewSet(viewsets.ModelViewSet):
    # queryset = YeuCauTuyenDung.objects.all()
    serializer_class = YeuCauTuyenDungSerializer

    def get_queryset(self):
        if self.action == 'list':
            if hasattr(self.request.user, 'nguoi_tim_viec'):
                return YeuCauTuyenDung.objects.filter(nguoi_tim_viec=self.request.user.nguoi_tim_viec)
            elif hasattr(self.request.user, 'nha_tuyen_dung'):
                viec_lam_ids = ViecLam.objects.filter(nha_tuyen_dung=self.request.user.nha_tuyen_dung).values_list('id',
                                                                                                                   flat=True)
                return YeuCauTuyenDung.objects.filter(viec_lam_id__in=viec_lam_ids)
        return YeuCauTuyenDung.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsNguoiTimViec()]
        elif self.action == 'destroy' or self.action == 'list':
            return [permissions.IsAuthenticated(), IsAdminOrReadOnly()]
        elif self.action == 'cap_nhat_trang_thai':
            return [permissions.IsAuthenticated(), IsNhaTuyenDung()]
        elif self.action == 'retrieve':
            return [permissions.IsAuthenticated(), IsNguoiTimViecXemYeuCauTuyenDung() | IsNhaTuyenDungXemVaChamKetQua()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        nguoi_tim_viec = getattr(request.user, 'nguoi_tim_viec', None)
        if not nguoi_tim_viec:
            return Response({"error": "Tài khoản không phải là người tìm việc."}, status=status.HTTP_403_FORBIDDEN)

        cv_id = request.data.get('cv')
        viec_lam_id = request.data.get('viec_lam')

        try:
            cv = CV.objects.get(id=cv_id, nguoi_tim_viec=nguoi_tim_viec)
            viec_lam = ViecLam.objects.get(id=viec_lam_id)
        except CV.DoesNotExist:
            return Response({"error": "CV không tồn tại hoặc không thuộc bạn."}, status=status.HTTP_400_BAD_REQUEST)
        except ViecLam.DoesNotExist:
            return Response({"error": "Việc làm không tồn tại."}, status=status.HTTP_400_BAD_REQUEST)

        if YeuCauTuyenDung.objects.filter(nguoi_tim_viec=nguoi_tim_viec, viec_lam=viec_lam).exists():
            return Response({"error": "Bạn đã ứng tuyển công việc này rồi."}, status=status.HTTP_400_BAD_REQUEST)

        yeu_cau = YeuCauTuyenDung.objects.create(
            cv=cv,
            nguoi_tim_viec=nguoi_tim_viec,
            viec_lam=viec_lam,
            ket_qua_ho_so=False,
            ket_qua_tuyen_dung=False
        )

        return Response(self.get_serializer(yeu_cau).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='cap-nhat-trang-thai')
    def cap_nhat_trang_thai(self, request, pk=None):
        ung_tuyen = self.get_object()

        permission = IsNhaTuyenDungXemVaChamKetQua()
        if not permission.has_object_permission(request, self, ung_tuyen):
            return Response({"error": "Bạn không có quyền cập nhật trạng thái ứng tuyển này."},
                            status=status.HTTP_403_FORBIDDEN)

        # Cập nhật trạng thái từ request
        for field in ['danh_gia_ho_so', 'ket_qua_ho_so', 'ket_qua_tuyen_dung']:
            if field in request.data:
                setattr(ung_tuyen, field, request.data[field])

        ung_tuyen.save()
        return Response(self.get_serializer(ung_tuyen).data)