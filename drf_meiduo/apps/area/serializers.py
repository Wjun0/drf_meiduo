import re
from rest_framework import serializers
from area.models import Area
from drf_meiduo.apps.users.models import Address



class AddressSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    district_id = serializers.IntegerField()
    class Meta:
        model = Address
        fields = ('id','title','tel','receiver','province','place','mobile','email','district','city','province_id','city_id','district_id')
        # exclude = ('user','is_deleted','create_time','update_time')
        extra_kwargs = {
            'id':{'read_only':True}
        }

    def validate(self, attrs):
        mobile = attrs['mobile']
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            raise serializers.ValidationError('手机号格式不对！')

        return attrs

    def create(self, validated_data):
        # 添加请求的user
        validated_data['user'] = self.context['request'].user
        obj = Address.objects.create(**validated_data)
        return obj



class AreaSearializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id','name')
        extra_kwargs = {
            'id':{
                'read_only':True
            },
            'name':{
                'read_only':True
            }
        }



class RetriverAreasSerializer(serializers.ModelSerializer):
    subs = AreaSearializer(many=True,read_only=True)

    class Meta:
        model = Area
        fields = ('id','name','subs')