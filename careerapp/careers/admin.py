# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path

from .models import (
    NguoiDung,
    NguoiTimViec,
    NhaTuyenDung,
    ViecLam,
    CV,
    YeuCauTuyenDung,
    HoiThoai,
    TinNhan,
    ThongBao,
    PhongVan
)


class CVInlineAdmin(admin.StackedInline):
    model = CV
    fk_name = 'nguoi_tim_viec'


@admin.register(NguoiDung)
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


class NguoiTimViecAdmin(admin.ModelAdmin):
    inlines = [CVInlineAdmin]


class CareerAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống tìm việc trực tuyến'

    def get_urls(self):
        return [path('career-stats/', self.stats_view)] + super().get_urls()

    def stats_view(self, request):
        count = ViecLam.objects.filter(is_active=True).count()
        stats = ViecLam.objects.annotate(CV_count=Count('yeucautuyendung')).values('id', 'tenCongViec', 'CV_count')
        return TemplateResponse(request, 'admin/career-stats.html', {
            'career_count': count,
            'career_stats': stats,
        })


admin_site = CareerAppAdminSite(name='eCareer')
admin_site.register(NguoiDung, NguoiDungAdmin)
admin_site.register(NguoiTimViec, NguoiTimViecAdmin)
admin_site.register(NhaTuyenDung)
admin_site.register(ViecLam)
admin_site.register(CV)
admin_site.register(YeuCauTuyenDung)
admin_site.register(HoiThoai)
admin_site.register(TinNhan)
admin_site.register(PhongVan)
admin_site.register(ThongBao)