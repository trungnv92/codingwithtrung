from rest_framework import serializers
from account.models import Account
from django.contrib.auth import password_validation

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def save(self):
        account = Account(email=self.validated_data['email'], username=self.validated_data['username'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords much match.'})
        account.set_password(password)
        account.save()
        return account

class ChangePasswordSerializer1(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'error': 'Your old password was entered incorrectly. Please enter it again.'})
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("The two password fields didn't match")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        print('vao day')
        password = self.validate_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'},required=True, write_only=True)
    new_password1 = serializers.CharField(style={'input_type': 'password'},required=True, write_only=True)

    # def validate_new_password(self, value):
    #     password_validation.validate_password(value)
    #     return value
    