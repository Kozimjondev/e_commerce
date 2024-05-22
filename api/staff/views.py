from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from api.staff.serializers import StaffSerializer, StaffDetailSerializer, StaffCreateSerializer

User = get_user_model()


class StaffCreateAPIView(CreateAPIView):
    serializer_class = StaffCreateSerializer


class StaffAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        print(request.user.username)
        return super().list(request, *args, **kwargs)


class StaffDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = StaffDetailSerializer
    lookup_field = 'guid'


class StaffUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = StaffCreateSerializer
    lookup_field = 'guid'
    permission_classes = (IsAuthenticated,)


class StaffDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = StaffCreateSerializer
    lookup_field = 'guid'
    permission_classes = (IsAuthenticated,)


# ViewSet option

class StaffAPIViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return StaffSerializer
        if hasattr(self, 'action') and self.action == 'retrieve':
            return StaffDetailSerializer
        return StaffCreateSerializer

    # lookup_field = 'guid'
    # permission_classes = (IsAuthenticated,)

"""
               This method is also good
"""

    # def list(self, request, *args, **kwargs):
    #     self.serializer_class = StaffSerializer
    #     return super().list(request, *args, **kwargs)





