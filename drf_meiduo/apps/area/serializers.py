
from rest_framework import serializers
from area.models import Area


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