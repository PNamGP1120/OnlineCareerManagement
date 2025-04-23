from rest_framework import viewsets, status, permissions, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password

from .models import NguoiDung, NguoiTimViec, NhaTuyenDung, ViecLam, CV, YeuCauTuyenDung
from .serializers import (
    NguoiDungSerializer, 
    NguoiTimViecSerializer, 
    NhaTuyenDungSerializer, 
    ViecLamSerializer, 
    CVSerializer, 
    YeuCauTuyenDungSerializer, 
    NguoiDungInfoSerializer
)
from .permissions import (
    IsAdminOrReadOnly, 
    IsNguoiTimViec, 
    IsNhaTuyenDung, 
    IsOwnerOrAdmin, 
    IsNguoiTimViecTaoYeuCauTuyenDung, 
    IsNguoiTimViecXemYeuCauTuyenDung, 
    IsNhaTuyenDungXemVaChamKetQua, 
    IsNguoiTimViecOrNhaTuyenDung
)

class NguoiDungViewSet(viewsets.ModelViewSet):
    queryset = NguoiDung.objects.filter(is_active=True)
    serializer_class = NguoiDungSerializer
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        elif self.action == 'nguoi_dung_hien_tai':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        # Create user account
        user = serializer.save()

    @action(detail=False, methods=['get'], url_path='nguoi-dung-hien-tai', permission_classes=[permissions.IsAuthenticated])
    def nguoi_dung_hien_tai(self, request):
        user = self.request.user
        return Response(NguoiDungInfoSerializer(user).data)


class NguoiTimViecViewSet(viewsets.ModelViewSet):
    queryset = NguoiTimViec.objects.all()
    serializer_class = NguoiTimViecSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsNguoiTimViec()]
        elif self.action == 'list':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Allow admin to access any profile
        if request.user.is_staff:
            return super().retrieve(request, *args, **kwargs)

        # Allow the profile owner to access their own
        if instance.nguoi_dung == request.user:
            return super().retrieve(request, *args, **kwargs)

        # Deny access if the user is neither the admin nor the profile owner
        return Response({"detail": "Bạn không có quyền xem thông tin người khác."}, status=status.HTTP_403_FORBIDDEN)


class NhaTuyenDungViewSet(viewsets.ModelViewSet):
    serializer_class = NhaTuyenDungSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return NhaTuyenDung.objects.all()
        elif hasattr(user, 'nha_tuyen_dung'):
            return NhaTuyenDung.objects.filter(nguoi_dung=user)
        return NhaTuyenDung.objects.none()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsNhaTuyenDung()]
        elif self.action == 'list':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class ViecLamViewSet(viewsets.ModelViewSet):
    serializer_class = ViecLamSerializer

    def get_queryset(self):
        queryset = ViecLam.objects.filter(is_active=True)
        if self.request.user.is_staff:
            return ViecLam.objects.all()
        if self.request.user.is_authenticated and hasattr(self.request.user, 'nha_tuyen_dung'):
            nha_tuyen_dung = NhaTuyenDung.objects.get(nguoi_dung=self.request.user)
            return queryset.filter(nha_tuyen_dung=nha_tuyen_dung)
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            if self.request.user.is_staff:
                return [permissions.IsAdminUser()]
            return [permissions.IsAuthenticated(), IsNhaTuyenDung()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise serializers.ValidationError("Bạn phải đăng nhập để thực hiện thao tác này.")
        try:
            nha_tuyen_dung = NhaTuyenDung.objects.get(nguoi_dung=self.request.user)
        except NhaTuyenDung.DoesNotExist:
            raise serializers.ValidationError("Bạn không phải là nhà tuyển dụng.")
        
        if ViecLam.objects.filter(
            tenCongViec=serializer.validated_data['tenCongViec'],
            viTriDangTuyen=serializer.validated_data['viTriDangTuyen'],
            diaChi=serializer.validated_data['diaChi'],
            ngayHetHan=serializer.validated_data['ngayHetHan'],
            nha_tuyen_dung=nha_tuyen_dung
        ).exists():
            raise serializers.ValidationError("Công việc này đã tồn tại.")
        serializer.save(nha_tuyen_dung=nha_tuyen_dung)


class ViecLamDetailAPIView(RetrieveAPIView):
    serializer_class = ViecLamSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ViecLam.objects.all()
        return ViecLam.objects.filter(is_active=True)


class CVViewSet(viewsets.ModelViewSet):
    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticated, IsNguoiTimViec | IsAdminOrReadOnly, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CV.objects.all()
        elif hasattr(user, 'nguoi_tim_viec'):
            return CV.objects.filter(nguoi_tim_viec=user.nguoi_tim_viec)
        return CV.objects.none()

    def perform_create(self, serializer):
        try:
            nguoi_tim_viec = self.request.user.nguoi_tim_viec
            serializer.save(nguoi_tim_viec=nguoi_tim_viec)
        except AttributeError:
            raise serializers.ValidationError("Người dùng không phải là người tìm việc.")


class YeuCauTuyenDungViewSet(viewsets.ModelViewSet):
    serializer_class = YeuCauTuyenDungSerializer

    def get_queryset(self):
        if self.action == 'list':
            if hasattr(self.request.user, 'nguoi_tim_viec'):
                return YeuCauTuyenDung.objects.filter(nguoi_tim_viec=self.request.user.nguoi_tim_viec)
            elif hasattr(self.request.user, 'nha_tuyen_dung'):
                viec_lam_ids = ViecLam.objects.filter(nha_tuyen_dung=self.request.user.nha_tuyen_dung).values_list('id', flat=True)
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
            return [permissions.IsAuthenticated(), IsNguoiTimViecOrNhaTuyenDung()]
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

        # Update status from request
        for field in ['danh_gia_ho_so', 'ket_qua_ho_so', 'ket_qua_tuyen_dung']:
            if field in request.data:
                setattr(ung_tuyen, field, request.data[field])

        ung_tuyen.save()
        return Response(self.get_serializer(ung_tuyen).data)
