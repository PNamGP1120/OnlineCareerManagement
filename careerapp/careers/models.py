from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

class NguoiDung(AbstractUser):
    hinh_dai_dien = CloudinaryField('image', 'hinh_dai_dien')
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

class NguoiTimViec(models.Model):
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, related_name='nguoi_tim_viec')  # OneToOneField liên kết trực tiếp với NguoiDung
    gioi_tinh = models.BooleanField()  # True cho nam, False cho nữ
    ngay_sinh = models.DateTimeField()
    so_dien_thoai = models.CharField(max_length=15)
    ky_nang = models.CharField(max_length=255)

    def __str__(self):
        return self.nguoi_dung.username

class NhaTuyenDung(models.Model):
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, related_name='nha_tuyen_dung')  # OneToOneField liên kết trực tiếp với NguoiDung
    ten_doanh_nghiep = models.CharField(max_length=255)
    website_doanh_nghiep = models.URLField()
    gioi_thieu_doanh_nghiep = models.TextField()
    linh_vuc_hoat_dong = models.CharField(max_length=255)
    dia_chi = models.CharField(max_length=255)
    hinh_anh_doanh_nghiep = CloudinaryField('image', 'hinh_anh_doanh_nghiep')

    def __str__(self):
        return self.ten_doanh_nghiep

class ViecLam(models.Model):
    tenCongViec = models.CharField(max_length=255)
    viTriDangTuyen = models.CharField(max_length=255)
    kinhNghiem = models.DateTimeField()
    mucLuong = models.IntegerField()
    diaChi = models.CharField(max_length=255)
    soLuongTuyen = models.IntegerField()
    doTuoi = models.IntegerField()
    hinhThucLamViec = models.CharField(max_length=50)
    bangCap = models.CharField(max_length=50)
    phucLoi = models.TextField()
    noiDungCongViec = models.TextField()
    yeuCauCongViec = models.TextField()
    thongTinLienHe = models.CharField(max_length=255)
    ngayTao = models.DateTimeField(auto_now_add=True)
    ngayCapNhat = models.DateTimeField(auto_now=True)
    ngayHetHan = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    # Mối quan hệ giữa công việc và nhà tuyển dụng
    nha_tuyen_dung = models.ForeignKey(NhaTuyenDung, on_delete=models.CASCADE, related_name='viec_lam')

    def __str__(self):
        return self.tenCongViec

class CV(models.Model):
    hinh_dai_dien = CloudinaryField('image', 'hinh_dai_dien')
    ho_ten = models.CharField(max_length=255)
    nghe_nghiep_ung_tuyen = models.CharField(max_length=255)
    bang_cap_cao_nhat = models.CharField(max_length=255)
    so_nam_kinh_nghiem = models.IntegerField()
    so_dien_thoai = models.CharField(max_length=255)
    email = models.EmailField()
    khu_vuc_lam_viec = models.CharField(max_length=255)
    dia_chi_chi_tiet = models.CharField(max_length=255)
    gioi_tinh = models.BooleanField()
    muc_luong_mong_muon = models.IntegerField()
    linkedln = models.URLField()
    muc_tieu_nghe_nghiep = models.TextField()
    ky_nang = models.CharField(max_length=255)
    thanh_tich = models.CharField(max_length=255)
    chung_nhan = models.CharField(max_length=255)
    so_thich = models.CharField(max_length=255)
    qua_trinh_hoat_dong = models.CharField(max_length=255)

    nguoi_tim_viec = models.ForeignKey(NguoiTimViec, on_delete=models.CASCADE, related_name='cv')

    def __str__(self):
        return f"{self.ho_ten} - {self.nghe_nghiep_ung_tuyen} ({self.so_nam_kinh_nghiem} năm KN)"


class YeuCauTuyenDung(models.Model):
    ngay_ung_tuyen = models.DateTimeField(auto_now_add=True)
    danh_gia_ho_so = models.CharField(max_length=255, null=True)
    ket_qua_ho_so = models.BooleanField()
    ket_qua_tuyen_dung = models.BooleanField()

    cv = models.OneToOneField(CV, on_delete=models.CASCADE)
    nguoi_tim_viec = models.ForeignKey(NguoiTimViec, on_delete=models.CASCADE)
    viec_lam = models.ForeignKey(ViecLam, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nguoi_tim_viec', 'viec_lam')
        verbose_name = 'Yêu cầu tuyển dụng'
        verbose_name_plural = 'Các yêu cầu tuyển dụng'

    def __str__(self):
        return f"{self.nguoi_tim_viec.nguoi_dung.username} ứng tuyển {self.viec_lam.tenCongViec}"


class HoiThoai(models.Model):
    thoi_gian_bat_dau = models.DateTimeField()
    thoi_gian_ket_thuc = models.DateTimeField()

    nguoi_tim_viec = models.ForeignKey(NguoiTimViec, on_delete=models.CASCADE)
    nha_tuyen_dung = models.ForeignKey(NhaTuyenDung, on_delete=models.CASCADE)

    def __str__(self):
        return f'Hội thoại giữa {self.nguoi_tim_viec.nguoi_dung.username} và {self.nha_tuyen_dung.nguoi_dung.username}'

class TinNhan(models.Model):
    nguoi_gui = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    da_doc=models.BooleanField()
    noi_dung=models.TextField()
    thoi_gian_gui_tin = models.DateTimeField()

    hoi_thoai = models.ForeignKey(HoiThoai, on_delete=models.CASCADE)

    def __str__(self):
        return f'Tin nhắn từ {self.nguoi_gui.username} lúc {self.thoi_gian_gui_tin}'

    def save(self, *args, **kwargs):
        if self.nguoi_gui != self.hoi_thoai.nguoi_tim_viec.nguoi_dung and self.nguoi_gui != self.hoi_thoai.nha_tuyen_dung.nguoi_dung:
            raise ValueError("Người gửi không nằm trong hội thoại này.")
        super().save(*args, **kwargs)

class PhongVan(models.Model):
    thoi_gian_phong_van = models.DateTimeField()
    video_URL = models.URLField()
    danh_gia = models.TextField()
    ket_qua_phong_van = models.BooleanField()

    yeu_cau_phong_van = models.ForeignKey(YeuCauTuyenDung, on_delete=models.CASCADE)

    def __str__(self):
        ung_vien = self.yeu_cau_phong_van.nguoi_tim_viec.nguoi_dung.username
        cong_viec = self.yeu_cau_phong_van.viec_lam.tenCongViec
        return f"Phỏng vấn: {ung_vien} - {cong_viec} ({self.thoi_gian_phong_van.strftime('%d/%m/%Y %H:%M')})"

class ThongBao(models.Model):
    noi_dung = models.TextField()

    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

    def __str__(self):
        return f"Thông báo đến {self.nguoi_dung.username}: {self.noi_dung[:50]}..."

