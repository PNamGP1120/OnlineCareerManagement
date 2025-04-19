# accounts/admin.py
from django.contrib import admin
from .models import (NguoiDung,
                     NguoiTimViec,
                     NhaTuyenDung,
                     ViecLam,
                     CV,
                     YeuCauTuyenDung,
                     HoiThoai,
                     TinNhan,ThongBao,
                     PhongVan)

# Admin cho NguoiDung
class NguoiDungAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'ngay_cap_nhat']
    search_fields = ['username', 'email']

admin.site.register(NguoiDung, NguoiDungAdmin)
admin.site.register(NguoiTimViec)
admin.site.register(NhaTuyenDung)
admin.site.register(ViecLam)
admin.site.register(CV)
admin.site.register(YeuCauTuyenDung)
admin.site.register(HoiThoai)
admin.site.register(TinNhan)
admin.site.register(PhongVan)