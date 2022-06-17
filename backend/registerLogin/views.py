from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        file = f'/Users/nitishgupta/Desktop/algoTrade/backend/strategiesAPI/user_files/{data["username"]}.py'
        open(file, 'a').close()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"data": {
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
        }
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        temp_list = super(LoginAPI, self).post(request, format=None)
        temp_list.data["username"] = user.username
        temp_list.data["email"] = user.email
        temp_list.data["aliceBlueID"] = user.aliceBlueID
        temp_list.data["isCredential"] = user.isCredential
        return Response({"data": temp_list.data})
