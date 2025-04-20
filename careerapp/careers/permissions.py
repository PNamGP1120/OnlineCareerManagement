from rest_framework import permissions

class IsNguoiTimViec(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'nguoi_tim_viec')

class IsNhaTuyenDung(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'nha_tuyen_dung')

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.nguoi_tim_viec == request.user.nguoi_tim_viec

class IsNguoiTimViecTaoYeuCauTuyenDung(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and hasattr(request.user, 'nguoi_tim_viec')
        return True

class IsNguoiTimViecXemYeuCauTuyenDung(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.nguoi_tim_viec == request.user.nguoi_tim_viec

class IsNhaTuyenDungXemVaChamKetQua(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'PATCH']:
            return obj.viec_lam.nha_tuyen_dung == request.user.nha_tuyen_dung
        return False
