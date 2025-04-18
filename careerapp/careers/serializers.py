# accounts/serializers.py
from rest_framework import serializers
from .models import NguoiDung, NguoiTimViec, NhaTuyenDung


class NguoiDungSerializer(serializers.ModelSerializer):
    hinh_dai_dien = serializers.SerializerMethodField()  # Trường hinh_dai_dien sẽ được tính toán thông qua phương thức này

    def get_hinh_dai_dien(self, obj):
        return obj.hinh_dai_dien.url if obj.hinh_dai_dien else None  # Trả về URL hình ảnh nếu có

    class Meta:
        model = NguoiDung
        fields = ['username', 'email', 'hinh_dai_dien', 'vai_tro', 'ngay_cap_nhat']
        extra_kwargs = {'password': {'write_only': True}}  # Mật khẩu không được trả về trong response

    def create(self, validated_data):
        data = validated_data.copy()
        user = NguoiDung(**data)
        user.set_password(user.password)
        user.save()
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['hinh_dai_dien'] = instance.hinh_dai_dien.url if instance.hinh_dai_dien else None
        return rep


# accounts/serializers.py
class NguoiTimViecSerializer(serializers.ModelSerializer):
    class Meta:
        model = NguoiTimViec
        fields = ['gioi_tinh', 'ngay_sinh', 'so_dien_thoai', 'email', 'ky_nang']


# accounts/serializers.py
class NhaTuyenDungSerializer(serializers.ModelSerializer):
    hinh_anh_doanh_nghiep = serializers.SerializerMethodField()

    def get_hinh_anh_doanh_nghiep(self, obj):
        return obj.hinh_anh_doanh_nghiep.url if obj.hinh_anh_doanh_nghiep else None

    class Meta:
        model = NhaTuyenDung
        fields = ['ten_doanh_nghiep', 'website_doanh_nghiep', 'gioi_thieu_doanh_nghiep', 'linh_vuc_hoat_dong',
                  'dia_chi', 'hinh_anh_doanh_nghiep']
