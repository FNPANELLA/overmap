from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
                    'first_name': {'required': False},
                    'last_name': {'required': False}
                }
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    