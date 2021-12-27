from rest_framework import serializers
from .models import VisitorUser


class VisitorUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitorUser
        fields = ("id", "usernm", "signupdt", "u_segmt")
        # fields = '__all__'


class VisitorBasicSerializer(serializers.Serializer):
    usernm = serializers.CharField(max_length=50)
    signupdt = serializers.DateTimeField()
    u_segmt = serializers.CharField(max_length=5)

    def create(self, validated_data):
        return VisitorUser.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.usernm = validated_data.get('usernm', instance.usernm)
        instance.signupdt = validated_data.get('signupdt', instance.signupdt)
        instance.u_segmt = validated_data.get('u_segmt', instance.u_segmt)
        instance.save()

        return instance
