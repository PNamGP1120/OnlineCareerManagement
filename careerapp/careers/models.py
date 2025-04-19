from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from ckeditor.fields import RichTextField

# ======= Enum Choices =======
class BangCapChoices(models.TextChoices):
    TRUNG_CAP = 'TC', 'Trung cấp'
    CAO_DANG = 'CD', 'Cao đẳng'
    DAI_HOC = 'DH', 'Đại học'
    THAC_SI = 'TS', 'Thạc sĩ'
    TIEN_SI = 'TSI', 'Tiến sĩ'


class HinhThucLamViecChoices(models.TextChoices):
    TOAN_THOI_GIAN = 'FT', 'Toàn thời gian'
    BAN_THOI_GIAN = 'PT', 'Bán thời gian'
    THUC_TAP = 'TT', 'Thực tập'
    FREELANCE = 'FR', 'Freelance'


# ======= Người dùng chính =======
class NguoiDung(AbstractUser):
    hinh_dai_dien = models.ImageField(upload_to='avatars/', null=True, blank=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)


# ======= Người tìm việc =======
class NguoiTimViec(models.Model):
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE)
    gioi_tinh = models.BooleanField(null=True)
    ngay_sinh = models.DateField(null=True, blank=True)
    so_dien_thoai = models.CharField(max_length=20)
    email = models.EmailField()
    ky_nang = models.TextField()


# ======= Nhà tuyển dụng =======
class NhaTuyenDung(models.Model):
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE)
    ten_doanh_nghiep = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    gioi_thieu = RichTextField()
    linh_vuc_hoat_dong = models.CharField(max_length=255)
    dia_chi = models.CharField(max_length=255)
    hinh_anh = models.ImageField(upload_to='logos/', null=True, blank=True)


# ======= CV =======
class CV(models.Model):
    nguoi_tim_viec = models.ForeignKey(NguoiTimViec, on_delete=models.CASCADE)
    ho_ten = models.CharField(max_length=255)
    nghe_nghiep = models.CharField(max_length=255)
    bang_cap = models.CharField(max_length=10, choices=BangCapChoices.choices)
    so_nam_kinh_nghiem = models.PositiveIntegerField()
    email = models.EmailField(null=True, blank=True)
    so_dien_thoai = models.CharField(max_length=20)
    dia_chi = models.CharField(max_length=255, default='Chưa cập nhật')
    ky_nang = models.TextField()
    thanh_tich = models.TextField(blank=True)
    muc_luong_mong_muon = models.PositiveIntegerField()
    muc_tieu_nghe_nghiep = models.TextField()
    so_thich = models.TextField(blank=True)
    chung_nhan = models.TextField(blank=True)
    khu_vuc_lam_viec = models.CharField(max_length=255)
    thong_tin_khac = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)


# ======= Việc làm =======
class ViecLam(models.Model):
    nha_tuyen_dung = models.ForeignKey(NhaTuyenDung, on_delete=models.CASCADE)
    tieu_de = models.CharField(max_length=255)
    vi_tri = models.CharField(max_length=255)
    muc_luong = models.PositiveIntegerField()
    dia_chi = models.CharField(max_length=255)
    hinh_thuc_lam_viec = models.CharField(max_length=10, choices=HinhThucLamViecChoices.choices, default='FT')
    bang_cap = models.CharField(max_length=10, choices=BangCapChoices.choices)
    kinh_nghiem = models.DurationField()
    phuc_loi = models.TextField()
    yeu_cau = models.TextField()
    mo_ta = models.TextField()
    so_luong_tuyen = models.PositiveIntegerField()
    do_tuoi = models.PositiveIntegerField()
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    ngay_het_han = models.DateTimeField()
    duyet = models.BooleanField(default=False)


# ======= Yêu cầu tuyển dụng =======
class YeuCauTuyenDung(models.Model):
    viec_lam = models.ForeignKey(ViecLam, on_delete=models.CASCADE)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    ngay_ung_tuyen = models.DateTimeField(auto_now_add=True)
    danh_gia = models.TextField(blank=True)
    ket_qua_ho_so = models.BooleanField(null=True)
    ket_qua_tuyen_dung = models.BooleanField(null=True)


# ======= Phỏng vấn =======
class PhongVan(models.Model):
    yeu_cau = models.OneToOneField(YeuCauTuyenDung, on_delete=models.CASCADE)
    thoi_gian = models.DateTimeField()
    video_url = models.URLField()
    danh_gia = models.TextField()
    ket_qua = models.BooleanField(null=True)


# ======= Hội thoại & Tin nhắn =======
class HoiThoai(models.Model):
    thoi_gian_bat_dau = models.DateTimeField(auto_now_add=True)
    thoi_gian_ket_thuc = models.DateTimeField(null=True, blank=True)


class TinNhan(models.Model):
    hoi_thoai = models.ForeignKey(HoiThoai, on_delete=models.CASCADE, null=True, blank=True, related_name='tin_nhan')
    nguoi_gui = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='tin_gui')
    nguoi_nhan = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='tin_nhan')
    noi_dung = models.TextField()
    thoi_gian_gui_tin = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


# ======= Thông báo =======
class ThongBao(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    noi_dung = models.TextField()
    da_doc = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)