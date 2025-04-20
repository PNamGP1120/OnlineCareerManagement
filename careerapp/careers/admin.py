# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (NguoiDung,
                     NguoiTimViec,
                     NhaTuyenDung,
                     ViecLam,
                     CV,
                     YeuCauTuyenDung,
                     HoiThoai,
                     TinNhan,ThongBao,
                     PhongVan)

class NguoiDungAdmin(UserAdmin):
    model = NguoiDung
    list_display = ('username', 'email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'hinh_dai_dien')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'hinh_dai_dien', 'is_staff', 'is_active'),
        }),
    )

admin.site.register(NguoiDung, NguoiDungAdmin)
admin.site.register(NguoiTimViec)
admin.site.register(NhaTuyenDung)
admin.site.register(ViecLam)
admin.site.register(CV)
admin.site.register(YeuCauTuyenDung)
admin.site.register(HoiThoai)
admin.site.register(TinNhan)
admin.site.register(PhongVan)