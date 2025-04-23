import re
from rest_framework import serializers
from .models import (
    NguoiDung, NguoiTimViec, NhaTuyenDung,
    ViecLam, CV, YeuCauTuyenDung
)

# ============================== #
#      Serializers người dùng    #
# ============================== #

class NguoiDungInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NguoiDung
        fields = ['username', 'email', 'first_name', 'last_name', 'hinh_dai_dien']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['hinh_dai_dien'] = instance.hinh_dai_dien.url if instance.hinh_dai_dien else None
        return rep


class NguoiDungSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = NguoiDung
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'hinh_dai_dien']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Mật khẩu và mật khẩu xác nhận không khớp.")

        if not self.is_strong_password(password):
            raise serializers.ValidationError(
                "Mật khẩu không đủ mạnh. Phải có ít nhất 8 ký tự, một chữ cái viết hoa, một số và một ký tự đặc biệt."
            )
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = NguoiDung(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['hinh_dai_dien'] = instance.hinh_dai_dien.url if instance.hinh_dai_dien else None
        return rep

    def is_strong_password(self, password):
        return (
            len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'\d', password) and
            re.search(r'[\W_]', password)
        )

# ===================================== #
#     Serializers cho Người Tìm Việc    #
# ===================================== #

class NguoiTimViecSerializer(serializers.ModelSerializer):
    nguoi_dung_thong_tin = NguoiDungSerializer(source='nguoi_dung', read_only=True)
    nguoi_dung = serializers.PrimaryKeyRelatedField(queryset=NguoiDung.objects.all())

    class Meta:
        model = NguoiTimViec
        fields = ['nguoi_dung', 'nguoi_dung_thong_tin', 'gioi_tinh', 'ngay_sinh', 'so_dien_thoai', 'ky_nang']

# ===================================== #
#    Serializers cho Nhà Tuyển Dụng     #
# ===================================== #

class NhaTuyenDungSerializer(serializers.ModelSerializer):
    nguoi_dung_thong_tin = NguoiDungSerializer(source='nguoi_dung', read_only=True)
    nguoi_dung = serializers.PrimaryKeyRelatedField(queryset=NguoiDung.objects.all())

    class Meta:
        model = NhaTuyenDung
        fields = [
            'nguoi_dung', 'nguoi_dung_thong_tin',
            'ten_doanh_nghiep', 'website_doanh_nghiep',
            'gioi_thieu_doanh_nghiep', 'linh_vuc_hoat_dong',
            'dia_chi', 'hinh_anh_doanh_nghiep'
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['hinh_anh_doanh_nghiep'] = instance.hinh_anh_doanh_nghiep.url if instance.hinh_anh_doanh_nghiep else None
        return rep

# ================================= #
#    Serializers cho Việc Làm       #
# ================================= #

class ViecLamSerializer(serializers.ModelSerializer):
    nha_tuyen_dung = NhaTuyenDungSerializer(read_only=True)

    class Meta:
        model = ViecLam
        fields = [
            'id', 'tenCongViec', 'viTriDangTuyen', 'kinhNghiem', 'mucLuong',
            'diaChi', 'soLuongTuyen', 'doTuoi', 'hinhThucLamViec', 'bangCap',
            'phucLoi', 'noiDungCongViec', 'yeuCauCongViec', 'thongTinLienHe',
            'ngayHetHan', 'ngayTao', 'ngayCapNhat', 'is_active', 'nha_tuyen_dung'
        ]

    def validate(self, data):
        if ViecLam.objects.filter(
            tenCongViec=data['tenCongViec'],
            viTriDangTuyen=data['viTriDangTuyen'],
            diaChi=data['diaChi'],
            ngayHetHan=data['ngayHetHan']
        ).exists():
            raise serializers.ValidationError("Công việc này đã tồn tại.")
        return data

    def create(self, validated_data):
        nha_tuyen_dung = NhaTuyenDung.objects.get(nguoi_dung=self.context['request'].user)
        validated_data['nha_tuyen_dung'] = nha_tuyen_dung
        return super().create(validated_data)

# ============================== #
#    Serializers cho CV         #
# ============================== #

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = '__all__'
        read_only_fields = ['nguoi_tim_viec']

# =========================================== #
#  Serializers cho Yêu Cầu Tuyển Dụng (Apply) #
# =========================================== #

class YeuCauTuyenDungSerializer(serializers.ModelSerializer):
    class Meta:
        model = YeuCauTuyenDung
        fields = [
            'id', 'cv', 'nguoi_tim_viec', 'viec_lam',
            'danh_gia_ho_so', 'ket_qua_ho_so', 'ket_qua_tuyen_dung'
        ]
        read_only_fields = ['ngay_ung_tuyen', 'ngay_cat_nhat']
