from django.contrib.auth import logout
from django.core.serializers import serialize
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Person
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import SingUpSerializerUser, SingUpSerializerPerson
# import project
# from project.reservations.serializer import FavouritSerializer, MyReservationsSerializer, MyRealEstatesSerializer
# from project.project import settings

# views.py (for signup1)
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Person
from .serializers import SingUpSerializerUser, SingUpSerializerPerson

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response({
        'username': request.user.username,
        'email': request.user.email
    })

User = get_user_model()

class UserSignUpView(APIView):
    def post(self, request):
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'confirm_password': request.data.get('confirm_password'),
        }

        # Validate user data
        user_serializer = SingUpSerializerUser(data=user_data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = user_serializer.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'User registered successfully',
                'user_id': user.id,
                'access': str(refresh.access_token),  # Access token
                'refresh': str(refresh),  # Refresh token
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # If anything fails, delete the user if it was created
            if 'user' in locals():
                user.delete()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.permissions import IsAuthenticated

class PersonSignUpView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the request is authenticated

    def post(self, request):
        person_data = {
            'phone': request.data.get('phone'),
            'city': request.data.get('city'),
            'email': request.data.get('email'),
            'name': request.data.get('name'),
        }

        user = request.user  # Extract the authenticated user from the token

        # Validate person data
        person_serializer = SingUpSerializerPerson(data=person_data)
        if not person_serializer.is_valid():
            return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            person = person_serializer.save(user=user)  # Link person to the authenticated user

            return Response({
                'message': 'Person data registered successfully',
                'person_id': person.id,
                'user_id': user.id,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@method_decorator(csrf_exempt, name='dispatch')
class logout_view(APIView):
    permission_classes = [IsAuthenticated]
    print("hhhhhhhhhii   ")
    def post(self, request):
        print("\n\n=== REACHED LOGOUT VIEW ===")  # Add this
        print("Headers:", request.headers)  # Debug headers
        print("Body:", request.data)  # Debug body
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
        data=request.data
        user = request.user
        print('3        ', user.first_name)

        person=user.person
        if data['confirm_password'] ==data['password'] :
            person.name=data['name']
            person.email=data['email']
            user.username=data['username']
            user.set_password(data['password'])
            user.save()

            person.city=data['city']
            person.phone=data['phone']
            person.user=user
            person.save()
            serializer_user = SingUpSerializerUser(user, many=False)
            serializer_person = SingUpSerializerPerson(person, many=False)

            return Response({'details':'Your account modifyed successfully!' ,
                             'user': serializer_user.data,
                             'person': serializer_person.data
                             },
                    status=status.HTTP_201_CREATED
                    )
        else:
                return Response({'error':'reenter your password '},status=status.HTTP_400_BAD_REQUEST)


