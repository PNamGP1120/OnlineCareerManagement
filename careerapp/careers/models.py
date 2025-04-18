# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

class NguoiDung(AbstractUser):
    hinh_dai_dien = CloudinaryField('hinh_dai_dien', 'hinh_dai_dien')
    vai_tro = models.CharField(max_length=50, choices=[('nha_tuyen_dung', 'Nhà Tuyển Dụng'), ('nguoi_tim_viec', 'Người Tìm Việc')], default='nguoi_tim_viec')
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

# accounts/models.py
class NguoiTimViec(models.Model):
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, related_name='nguoi_tim_viec')
    gioi_tinh = models.BooleanField()  # True cho nam, False cho nữ
    ngay_sinh = models.DateTimeField()
    so_dien_thoai = models.CharField(max_length=15)
    ky_nang = models.CharField(max_length=255)

    def __str__(self):
        return self.nguoi_dung.username


# accounts/models.py
class NhaTuyenDung(models.Model):
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, related_name='nha_tuyen_dung')
    ten_doanh_nghiep = models.CharField(max_length=255)
    website_doanh_nghiep = models.URLField()
    gioi_thieu_doanh_nghiep = models.TextField()
    linh_vuc_hoat_dong = models.CharField(max_length=255)
    dia_chi = models.CharField(max_length=255)
    hinh_anh_doanh_nghiep = CloudinaryField('hinh_dai_doanh_nghiep', 'hinh_anh_doanh_nghiep')

    def __str__(self):
        return self.ten_doanh_nghiep
