# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin_ak_sk.models import AkSkManage, ConsumerSecretKeyGenerator


class AkSkManageSerializer(CustomModelSerializer):
    """
    ak/sk 管理 -序列化器
    """

    class Meta:
        model = AkSkManage
        fields = "__all__"
        read_only_fields = ["id"]


class AkSkManageUpdateSerializer(CustomModelSerializer):
    """
     ak/sk 管理 更新时的列化器
    """
    name = serializers.CharField(required=False)

    class Meta:
        model = AkSkManage
        fields = '__all__'

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        validated_data['access_key'] = ConsumerSecretKeyGenerator('access_key')()
        validated_data['access_secret'] = ConsumerSecretKeyGenerator('access_secret')()
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance


class AkSkManageViewSet(CustomModelViewSet):
    """
    ak/sk 管理接口:
    """
    queryset = AkSkManage.objects.all()
    serializer_class = AkSkManageSerializer

    @action(methods=["PUT"], detail=True)
    def update_key(self, request, *args, **kwargs):
        self.serializer_class = AkSkManageUpdateSerializer
        return super().update(request, *args, **kwargs)
