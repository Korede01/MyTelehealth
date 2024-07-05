import random
import string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import serializers
from hospital.models import Hospital

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class HospitalSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Hospital
        fields = ['id', 'name', 'address', 'contact_number', 'email', 'unique_id', 'licensing_information', 'data_security_agreement']
        read_only_fields = ['unique_id']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = User.objects.make_random_password(length=20)

        # Ensure the username is unique
        username = self.generate_unique_username(validated_data['name'])

        user = User.objects.create_user(username=username, email=email, password=password)

        # Generate unique_id
        validated_data['unique_id'] = self.generate_unique_id(validated_data['name'])

        # Create the hospital instance without the 'user' field
        hospital = Hospital(**validated_data)

        # Manually set the user field and save the hospital instance
        hospital.user = user
        hospital.save()

        # Send email to hospital with initial password and username
        self.send_initial_password_email(user, password)

        return hospital

    def generate_unique_username(self, email):
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username

    def generate_unique_id(self, name):
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        unique_id = f"{name[:3].upper()}{random_string}"
        return unique_id

    def send_initial_password_email(self, user, password):
        send_mail(
            'Your Hospital Account Details',
            f'Hello, your hospital account has been created.\n\nUsername: {user.username}\nEmail: {user.email}\nPassword: {password}\n\nPlease change your password after logging in.',
            'erinlekorede@gmail.com',
            [user.email],
            fail_silently=False,
        )


