from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


# ======= Người dùng chính =======
class NguoiDung(AbstractUser):
    hinh_dai_dien = CloudinaryField('avatars', 'hinh_dai_dien')
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    xem_thong_bao = models.ManyToManyField('ThongBao', through='NguoiDungXemThongBao')

# ======= Thông báo =======
class ThongBao(models.Model):
    noi_dung = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# ======= Thời điểm xem thông báo gần nhất của người dùng =======
class NguoiDungXemThongBao(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    thong_bao = models.ForeignKey(ThongBao, on_delete=models.CASCADE)
    ngay_xem_gan_nhat = models.DateTimeField(auto_now=True)
    da_doc = models.BooleanField(default=False)

    class Meta:
        unique_together = ('nguoi_dung', 'thong_bao')

# ======= Người tìm việc =======
class NguoiTimViec(models.Model):
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, related_name='nguoi_tim_viec')  # OneToOneField liên kết trực tiếp với NguoiDung
    gioi_tinh = models.BooleanField()  # True cho nam, False cho nữ
    ngay_sinh = models.DateTimeField()
    so_dien_thoai = models.CharField(max_length=15)
    ky_nang = models.CharField(max_length=255)

    def __str__(self):
        return self.nguoi_dung.username

# ======= Nhà tuyển dụng =======
class NhaTuyenDung(models.Model):
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, related_name='nha_tuyen_dung')  # OneToOneField liên kết trực tiếp với NguoiDung
    ten_doanh_nghiep = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    gioi_thieu = RichTextField()
    linh_vuc_hoat_dong = models.CharField(max_length=255)
    dia_chi = models.CharField(max_length=255)
    hinh_anh = CloudinaryField('logos', null=True, blank=True)


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
    ngay_cat_nhat = models.DateTimeField(auto_now=True)
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
    nguoi_gui = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, ralated_name='tin_gui')
    nguoi_nhan = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, related_name='tin_nhan')
    da_doc=models.BooleanField(default=False)
    noi_dung=models.TextField()
    thoi_gian_gui_tin = models.DateTimeField()

    hoi_thoai = models.ForeignKey(HoiThoai, on_delete=models.CASCADE, null=True, blank=True, related_name='tin_nhan')

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

