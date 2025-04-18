from django.contrib import admin

from .models import NguoiDung, NguoiTimViec, NhaTuyenDung

admin.site.register(NguoiDung)
admin.site.register(NguoiTimViec)
admin.site.register(NhaTuyenDung)
