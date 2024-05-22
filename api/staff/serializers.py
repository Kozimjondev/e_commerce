from django.contrib.auth import get_user_model, hashers
from rest_framework import serializers

User = get_user_model()


class StaffCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'},
                                     min_length=8)

    def validate_password(self, value):
        if value is None or len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters')
        if hashers.is_password_usable(value):
            print("Password is usable")
        password = hashers.make_password(value)
        return password

    class Meta:
        model = User
        fields = ('id', 'guid', 'username', 'name', 'password')


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'guid', 'username', 'name', )


class StaffDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
