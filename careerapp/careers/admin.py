from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import NguoiDung, NguoiTimViec, NhaTuyenDung


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

admin.site.register(NguoiDung)
admin.site.register(NguoiTimViec)
admin.site.register(NhaTuyenDung ,NhaTuyenDungAdmin)
