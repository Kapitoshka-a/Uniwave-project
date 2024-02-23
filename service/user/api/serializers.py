from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_repeat']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        password = self.validated_data['password']
        password_repeat = self.validated_data['password_repeat']

        if password != password_repeat:
            raise serializers.ValidationError({'error': 'Перший пароль повинен співпадати з другим'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Електронна адреса уже була зареєстрована'})

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Incorrect username or password.')
        data['user'] = user
        return data
