# users/api_serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['role'] = getattr(user, 'role', '')
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # add extra responses here
        data['username'] = self.user.username
        data['role'] = getattr(self.user, 'role', '')
        return data
