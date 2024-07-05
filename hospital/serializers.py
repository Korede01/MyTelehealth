import re, random, csv
import xml.etree.ElementTree as ET
from io import StringIO
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import Appointment, Role
from doctor.models import Doctor
from patient.models import Patient

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

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def process_csv(self, file, hospital):
        decoded_file = file.read().decode('utf-8')
        io_string = StringIO(decoded_file)
        reader = csv.reader(io_string)
        headers = next(reader)
        print(f"CSV Headers: {headers}")  # Debug statement
        
        for row in reader:
            data = dict(zip(headers, row))
            print(f"CSV Row Data: {data}")  # Debug statement
            self.create_user(data, hospital)

    def process_xml(self, file, hospital):
        tree = ET.parse(file)
        root = tree.getroot()
        
        for item in root.findall('item'):
            data = {child.tag: child.text for child in item}
            print(f"XML Item Data: {data}")  # Debug statement
            self.create_user(data, hospital)

    def create_user(self, data, hospital):
        role_name = data.get('role')
        try:
            role = Role.objects.get(name=role_name)
            print(f"Role found: {role_name}")  # Debug statement
        except Role.DoesNotExist:
            print(f"Role not found: {role_name}")  # Debug statement
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        if role_name == 'Doctor':
            self.create_doctor(data, hospital, role)
        elif role_name == 'Patient':
            self.create_patient(data, hospital, role)

    def create_doctor(self, data, hospital, role):
        username = self.generate_username(data['first_name'], data['last_name'])
        password = User.objects.make_random_password(length=20)
        user = User.objects.create_user(
            username=username,
            email=data['email'],
            password=password,
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.save()
        doctor = Doctor.objects.create(
            user=user,
            hospital=hospital,
            specialization=data['specialization'],
            contact_number=data['contact_number'],
            role=role
        )
        doctor.save()
        print(f"Doctor created: {user.username}")  # Debug statement
        self.send_initial_password_email(user, password, hospital.name)

    def create_patient(self, data, hospital, role):
        username = self.generate_username(data['first_name'], data['last_name'])
        password = User.objects.make_random_password(length=20)
        user = User.objects.create_user(
            username=username,
            email=data['email'],
            password=password,
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.save()
        patient = Patient.objects.create(
            user=user,
            hospital=hospital,
            date_of_birth=data['date_of_birth'],
            contact_number=data['contact_number'],
            role=role
        )
        patient.save()
        print(f"Patient created: {user.username}")  # Debug statement
        self.send_initial_password_email(user, password, hospital.name)

    def generate_username(self, first_name, last_name):
        initials = f"{first_name}.{last_name[0].lower()}"
        unique_number = random.randint(1, 100)
        base_username = f"{initials}{unique_number}"
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username

    def send_initial_password_email(self, user, password, hospital_name):
        subject = 'Welcome to Our Telehealth Platform'
        message = (
            f"Dear {user.first_name},\n\n"
            f"You have been successfully onboarded to the telehealth platform by {hospital_name}.\n\n"
            f"Here are your login details:\n"
            f"Username: {user.username}\n"
            f"Password: {password}\n\n"
            f"Please go ahead and log in to your account at [platform URL]. For security reasons, "
            f"we strongly recommend that you change your password after your first login.\n\n"
            f"If you have any questions or need further assistance, please contact your hospital administrator.\n\n"
            f"Best regards,\n"
            f"The Telehealth Platform Team"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email='erinlekorede@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        print(f"Email sent to: {user.email}")  # Debug statement

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'reason', 'additional_details', 'start_time', 'end_time', 'status', 'created_at', 'updated_at']
