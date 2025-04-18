# careers/permissions.py
from rest_framework.permissions import BasePermission

class IsSuperUserPermission(BasePermission):
    """
    Chỉ cho phép superuser truy cập.
    """

    def has_permission(self, request, view):
        # Kiểm tra nếu người dùng là superuser
        if not request.user.is_superuser:
            self.message = "Bạn không có quyền thực hiện hành động này."  # Thông báo lỗi tùy chỉnh
            return False
        return True
