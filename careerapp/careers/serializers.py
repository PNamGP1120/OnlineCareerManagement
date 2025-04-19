import re

from rest_framework import serializers
from .models import NguoiDung, NguoiTimViec, NhaTuyenDung, ViecLam


class NguoiDungSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)  # Trường xác nhận mật khẩu

    class Meta:
        model = NguoiDung
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'hinh_dai_dien']
        extra_kwargs = {
            'password': {'write_only': True},  # Đảm bảo mật khẩu không bị trả về trong response
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        # Kiểm tra mật khẩu và mật khẩu xác nhận có trùng khớp không
        if password != confirm_password:
            raise serializers.ValidationError("Mật khẩu và mật khẩu xác nhận không khớp.")

        # Kiểm tra mật khẩu có đủ mạnh không
        if not self.is_strong_password(password):
            raise serializers.ValidationError(
                "Mật khẩu không đủ mạnh. Mật khẩu phải có ít nhất 8 ký tự, một chữ cái viết hoa, một chữ số và một ký tự đặc biệt.")

        # Tạo người dùng và mã hóa mật khẩu
        user = NguoiDung(**validated_data)
        user.set_password(password)  # Mã hóa mật khẩu trước khi lưu
        user.save()
        return user

    def to_representation(self, instance):
        # Đảm bảo chỉ trả về URL hình ảnh nếu có
        rep = super().to_representation(instance)
        if instance.hinh_dai_dien:
            rep['hinh_dai_dien'] = instance.hinh_dai_dien.url
        else:
            rep['hinh_dai_dien'] = None
        return rep

    def is_strong_password(self, password):
        """
        Kiểm tra mật khẩu có đủ mạnh hay không:
        - Ít nhất 8 ký tự
        - Một chữ cái viết hoa
        - Một chữ số
        - Một ký tự đặc biệt
        """
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):  # Kiểm tra chữ cái viết hoa
            return False
        if not re.search(r'[0-9]', password):  # Kiểm tra chữ số
            return False
        if not re.search(r'[\W_]', password):  # Kiểm tra ký tự đặc biệt
            return False
        return True



class NguoiTimViecSerializer(serializers.ModelSerializer):
    nguoi_dung = NguoiDungSerializer()

    class Meta:
        model = NguoiTimViec
        fields = ['nguoi_dung', 'gioi_tinh', 'ngay_sinh', 'so_dien_thoai', 'ky_nang']

class NhaTuyenDungSerializer(serializers.ModelSerializer):
    nguoi_dung = NguoiDungSerializer()

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Đảm bảo trả về URL của hình ảnh doanh nghiệp từ Cloudinary
        if instance.hinh_anh_doanh_nghiep:
            rep['hinh_anh_doanh_nghiep'] = instance.hinh_anh_doanh_nghiep.url
        else:
            rep['hinh_anh_doanh_nghiep'] = None

        return rep

    class Meta:
        model = NhaTuyenDung
        fields = ['nguoi_dung', 'ten_doanh_nghiep', 'website_doanh_nghiep', 'gioi_thieu_doanh_nghiep', 'linh_vuc_hoat_dong', 'dia_chi', 'hinh_anh_doanh_nghiep']



class ViecLamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViecLam
        fields = [
            'id',
            'tenCongViec',
            'viTriDangTuyen',
            'kinhNghiem',
            'mucLuong',
            'diaChi',
            'soLuongTuyen',
            'doTuoi',
            'hinhThucLamViec',
            'bangCap',
            'phucLoi',
            'noiDungCongViec',
            'yeuCauCongViec',
            'thongTinLienHe',
            'ngayHetHan',
            'diaChi',
            'ngayHetHan',
        ]
