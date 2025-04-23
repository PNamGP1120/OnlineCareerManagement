from rest_framework import permissions

class IsNguoiTimViec(permissions.BasePermission):
    """
    Chỉ cho phép người dùng là người tìm việc.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'nguoi_tim_viec')


class IsNhaTuyenDung(permissions.BasePermission):
    """
    Chỉ cho phép người dùng là nhà tuyển dụng.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'nha_tuyen_dung')


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Chỉ admin có thể ghi, người khác chỉ được xem (read-only).
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or 
            request.user and request.user.is_staff
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Chỉ chủ sở hữu hoặc admin có quyền thao tác với đối tượng.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or getattr(obj, 'nguoi_tim_viec', None) == getattr(request.user, 'nguoi_tim_viec', None)


class IsNguoiTimViecTaoYeuCauTuyenDung(permissions.BasePermission):
    """
    Chỉ người tìm việc mới có thể tạo yêu cầu tuyển dụng (POST).
    """
    def has_permission(self, request, view):
        return request.method != 'POST' or hasattr(request.user, 'nguoi_tim_viec')


class IsNguoiTimViecXemYeuCauTuyenDung(permissions.BasePermission):
    """
    Người tìm việc chỉ được xem yêu cầu tuyển dụng của chính mình.
    """
    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'nguoi_tim_viec', None) == getattr(request.user, 'nguoi_tim_viec', None)


class IsNhaTuyenDungXemVaChamKetQua(permissions.BasePermission):
    """
    Nhà tuyển dụng chỉ được xem và cập nhật (PUT/PATCH) kết quả ứng tuyển nếu thuộc công việc của họ.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ['GET', 'PUT', 'PATCH'] and 
            getattr(obj.viec_lam, 'nha_tuyen_dung', None) == getattr(request.user, 'nha_tuyen_dung', None)
        )


class IsNguoiTimViecOrNhaTuyenDung(permissions.BasePermission):
    """
    Cho phép người dùng là người tìm việc hoặc nhà tuyển dụng,
    và chỉ cho phép thao tác với yêu cầu thuộc quyền của họ.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'nguoi_tim_viec') or hasattr(request.user, 'nha_tuyen_dung')

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'nguoi_tim_viec'):
            return obj.nguoi_tim_viec == request.user.nguoi_tim_viec
        if hasattr(request.user, 'nha_tuyen_dung'):
            return obj.viec_lam.nha_tuyen_dung == request.user.nha_tuyen_dung
        return False
