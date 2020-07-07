from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import UserProfile, Relation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'name',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('introduction', 'profile_image', 'background_image', 'user',)
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        instance.introduction = validated_data.get(
            'introduction', instance.introduction)
        instance.profile_image = validated_data.get(
            'profile_image', instance.profile_image)
        instance.background_image = validated_data.get(
            'background_image', instance.background_image)
        user_data = validated_data.get('user')
        instance.user.name = user_data.get('name')
        instance.user.save()
        instance.save()
        return instance


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ('id', 'follower', 'target',)
