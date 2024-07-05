import re
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Doctor
from hospital.models import Hospital

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        
        """
        Check that the new password meets the required criteria:
        - At least 8 characters long
        - Contains both uppercase and lowercase letters
        - Contains at least one digit
        - Contains at least one special character
        """
        
        if len(value) < 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("New password must contain at least one uppercase letter.")
        
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("New password must contain at least one lowercase letter.")
        
        if not re.search(r'\d', value):
            raise serializers.ValidationError("New password must contain at least one digit.")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("New password must contain at least one special character.")
        
        return value

class DoctorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    hospital_name = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'hospital', 'hospital_name','first_name', 'last_name', 'email', 'specialization', 'contact_number', 'calendly_user', 'created_at', 'updated_at']
        
    def get_hospital_name(self, obj):
        return obj.hospital.name