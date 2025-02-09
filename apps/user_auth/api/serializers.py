from rest_framework import serializers
from apps.user_auth.models import User  # Dein Custom User Model importieren
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User  # Verwende dein eigenes User-Modell
        fields = ['email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError({'email': 'Ein Benutzer mit dieser E-Mail existiert bereits.'})
        return value

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise ValidationError({'password': 'Passwörter stimmen nicht überein.'})
        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')  # Brauchen wir nicht in der DB
        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'Kein Benutzer mit dieser E-Mail gefunden.'})

        user = authenticate(username=user.email, password=password)  # `username` zu `user.email` ändern

        if not user:
            raise serializers.ValidationError({'password': 'Falsches Passwort.'})

        data['user'] = user
        return data
