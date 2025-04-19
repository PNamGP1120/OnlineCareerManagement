from rest_framework import permissions

class IsNguoiTimViec(permissions.BasePermission):
    """
    Cho phép chỉ người dùng là Người tìm việc có thể truy cập.
    """
    def has_permission(self, request, view):
        # Chỉ cho phép người dùng có vai trò là "NguoiTimViec"
        return request.user and hasattr(request.user, 'nguoi_tim_viec')

class IsNhaTuyenDung(permissions.BasePermission):
    """
    Cho phép chỉ Nhà tuyển dụng có thể truy cập.
    """
    def has_permission(self, request, view):
        # Chỉ cho phép người dùng có vai trò là "NhaTuyenDung"
        return request.user and hasattr(request.user, 'nha_tuyen_dung')

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Quản trị viên có thể tạo, cập nhật, xóa. Người dùng khác chỉ có thể xem.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Cho phép xem thông tin
        return request.user and request.user.is_staff  # Chỉ cho phép admin thực hiện các phương thức khác
