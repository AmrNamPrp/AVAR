from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Person
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class SingUpSerializerUser(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        # fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')
        fields = ('username', 'password', 'confirm_password')
        extra_kwargs = {
            # 'first_name': {'required': True, 'allow_blank': False},
            # 'last_name': {'required': True, 'allow_blank': False},
            'username': {'required': True, 'allow_blank': False},
            # 'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8, 'write_only': True},
        }

    def validate(self, data):
        """
        Validate that the password and confirm_password match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def validate_password(self, value):
        """
        Validate the password using Django's built-in password validation.
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        validated_data.pop('confirm_password')  # Remove confirm_password from the data
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SingUpSerializerPerson(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('phone', 'city', 'email', 'name')
        extra_kwargs = {
            'city': {'required': True, 'allow_blank': False},
            'phone': {'required': True, 'allow_blank': False},
            'name': {'required': True, 'allow_blank': False},
            'email': {'required': False, 'allow_blank': True},
        }

    def validate_phone(self, value):
        """
        Validate that the phone number is unique.
        """
        if Person.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'username': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8, 'write_only': True},
        }


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'