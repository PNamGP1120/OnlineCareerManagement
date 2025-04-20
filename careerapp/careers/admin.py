# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import NguoiDung, NguoiTimViec, NhaTuyenDung, CV, ThongBao, NguoiDungXemThongBao


class NhaTuyenDungGioiThieuForm(forms.ModelForm):
    gioi_thieu = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = NhaTuyenDung
        fields = '__all__'

class NhaTuyenDungAdmin(admin.ModelAdmin):
    list_display = ['id','ten_doanh_nghiep','gioi_thieu']
    list_filter = ['ten_doanh_nghiep','gioi_thieu']
    search_fields = ['ten_doanh_nghiep']
    readonly_fields = ['image_view']

    def image_view(self, obj):
        if obj.hinh_anh:
            return mark_safe(f'<img src="{obj.hinh_anh.url}" width="120"/>')
        return "(Không có hình)"

    class Media:
        css = {
            'all': ('/media/static/css/style.css',)
        }
        js = ('media/static/js/main.js',)

    form = NhaTuyenDungGioiThieuForm


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

# Người tìm việc có thể thêm CV ngay tại phần nhập thông tin của họ
class CVInlineAdmin(admin.StackedInline):
    model = CV
    fk_name = 'nguoi_tim_viec'

class NguoiTimViecAdmin(admin.ModelAdmin):
    inlines = [CVInlineAdmin, ]

# Khi vào trang người dùng thì thấy được luôn những thông báo đã xem
class NguoiDungXemThongBaoInlineAdmin(admin.TabularInline):
    model = NguoiDungXemThongBao
    extra = 0
    fields = ('thong_bao', 'ngay_xem_gan_nhat', 'da_doc')
    readonly_fields = ('ngay_xem_gan_nhat',)

class NguoiDungAdmin(admin.ModelAdmin):
    inlines = [NguoiDungXemThongBaoInlineAdmin]

admin.site.register(NguoiDung, NguoiDungAdmin)
admin.site.register(ViecLam)
admin.site.register(CV)
admin.site.register(YeuCauTuyenDung)
admin.site.register(HoiThoai)
admin.site.register(TinNhan)
admin.site.register(PhongVan)
admin.site.register(ThongBao)
admin.site.register(NguoiTimViec, NguoiTimViecAdmin)
admin.site.register(NhaTuyenDung ,NhaTuyenDungAdmin)
