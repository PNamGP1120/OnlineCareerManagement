# accounts/views.py
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from .models import NguoiDung, NguoiTimViec, NhaTuyenDung
from .serializers import NguoiDungSerializer, NguoiTimViecSerializer, NhaTuyenDungSerializer
from .perms import IsSuperUserPermission
# careers/views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import NguoiDungSerializer


@api_view(['POST'])
def dang_ky_nguoi_dung(request):
    """
    API để đăng ký người dùng mới.
    """
    if request.method == 'POST':
        # Sử dụng serializer để xác thực dữ liệu người dùng
        serializer = NguoiDungSerializer(data=request.data)

        if serializer.is_valid():
            # Lưu người dùng mới
            user = serializer.save()

            # Trả về dữ liệu người dùng sau khi tạo thành công
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Nếu có lỗi trong quá trình xác thực dữ liệu
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NguoiDungViewSet(viewsets.ModelViewSet):
    queryset = NguoiDung.objects.all()
    serializer_class = NguoiDungSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

class NguoiTimViecViewSet(viewsets.ModelViewSet):
    queryset = NguoiTimViec.objects.all()
    serializer_class = NguoiTimViecSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserPermission)



class NhaTuyenDungViewSet(viewsets.ModelViewSet):
    queryset = NhaTuyenDung.objects.all()
    serializer_class = NhaTuyenDungSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserPermission)


