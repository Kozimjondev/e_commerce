from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from api.auth.serializers import LoginSerializer, LogoutSerializer, ChangePasswordSerializer, \
    AdminChangePasswordSerializer

User = get_user_model()


class LoginAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     # user = User.objects.filter(username=serializer.data.get('username')).first()
    #     # # user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
    #     # if user:
    #     #     refresh = RefreshToken.for_user(user)
    #     #
    #     #     return Response({
    #     #         'id': user.id,
    #     #         'guid': user.guid,
    #     #         'refresh': str(refresh),
    #     #         'access': str(refresh.access_token),
    #     #     })
    #     # return Response({"error": "Invalid credentials"})
    #     # return super().create(request, *args, **kwargs)


# class LogoutAPIView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#         try:
#             refresh = request.data['refresh']
#             print(refresh)
#             refresh_token = RefreshToken(refresh)
#             refresh_token.blacklist()
#
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'guid'

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return AdminChangePasswordSerializer
        return ChangePasswordSerializer
