from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.decorators import api_view, permission_classes
from account.api.serializers import RegistrationSerializer, ChangePasswordSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

@api_view(['POST'])
def registration_view(request):
    data = {}
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user'
            data['email'] = account.email
            data['token'] = Token.objects.get(user=account).key
            data['username'] = account.username
        else:
            data = serializer.errors
        return Response(data)



class ChangePasswordView(GenericAPIView):
    #serializer_class = ChangePasswordSerializer()
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset=None):

        return self.request.user
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            #check old pass
            old_password = serializer.data.get("old_password")
            
            if not self.object.check_password(old_password):
                return Response({"old_password a": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            
            #set_password new also hashes the password 
            self.object.set_password(serializer.data.get['new_password'])
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)