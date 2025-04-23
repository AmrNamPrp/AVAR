from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import SingUpSerializerUser, SingUpSerializerPerson
from rest_framework.permissions import IsAuthenticated
from .models import Person

# Now you can use generate_otp() where needed.

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


class PersonSignUpView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the request is authenticated

    def post(self, request):
        person_data = {
            'phone': request.data.get('phone'),
            'city': request.data.get('city'),
            'email': request.data.get('email'),
            'name': request.data.get('name'),
        }
        phone = request.data.get('phone')

        if len(phone) != 10 or phone[0] != '0':
            return Response({'error': 'enter a Syrian number'}, status=status.HTTP_303_SEE_OTHER)
        if Person.objects.filter(phone=phone).exists():
            return Response({'error': 'this number is already in use'}, status=status.HTTP_303_SEE_OTHER)

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
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def update_user_info(request):
#         data=request.data
#         user = request.user
#         print('3        ', user.first_name)
#
#         person=user.person
#         if data['confirm_password'] ==data['password'] :
#             person.name=data['name']
#             person.email=data['email']
#             user.username=data['username']
#             user.set_password(data['password'])
#             user.save()
#
#             person.city=data['city']
#             person.phone=data['phone']
#             person.user=user
#             person.save()
#             serializer_user = SingUpSerializerUser(user, many=False)
#             serializer_person = SingUpSerializerPerson(person, many=False)
#
#             return Response({'details':'Your account modifyed successfully!' ,
#                              'user': serializer_user.data,
#                              'person': serializer_person.data
#                              },
#                     status=status.HTTP_201_CREATED
#                     )
#         else:
#                 return Response({'error':'reenter your password '},status=status.HTTP_400_BAD_REQUEST)
#
#

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    data = request.data
    user = request.user
    try:
        person = user.person  # Assumes a OneToOne relationship
    except Exception as e:
        return Response({'error': 'No person profile found for the user.'},
                        status=status.HTTP_400_BAD_REQUEST)
    phone=data.get('phone')

    if len(phone)!=10 or phone[0]!='0' :
        return Response({'error': 'enter a Syrian number'}, status=status.HTTP_303_SEE_OTHER)



    # If either password field is provided, then both must be provided and must match.
    if ('password' in data or 'confirm_password' in data) and (data.get('password') or data.get('confirm_password')):
        if data.get('password') != data.get('confirm_password'):
            return Response({'error': 'Passwords do not match.'},
                            status=status.HTTP_400_BAD_REQUEST)




    # if data.get('phone')
    # Build the user_data dictionary. Only include password fields if a new password is provided.
    user_data = {'username': data.get('username')}
    if data.get('password'):
        user_data['password'] = data.get('password')
        user_data['confirm_password'] = data.get('confirm_password')
    print(22)
    # Build the person_data dictionary.
    person_data = {
        'phone': data.get('phone'),
        'city': data.get('city'),
        'email': data.get('email'),
        'name': data.get('name')
    }
    print(33)

    # Validate user data using the existing signup serializer (update mode)
    user_serializer = SingUpSerializerUser(instance=user, data=user_data, partial=True)
    if not user_serializer.is_valid():
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Validate person data using the signup serializer for Person (update mode)
    person_serializer = SingUpSerializerPerson(instance=person, data=person_data, partial=True)
    if not person_serializer.is_valid():
        return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if Person.objects.filter(phone=phone).exclude(user=user).exists():
        return Response({'error': 'This phone number is already in use.'}, status=status.HTTP_400_BAD_REQUEST)
    # Update the user instance.
    user.username = user_serializer.validated_data.get('username', user.username)
    if 'password' in user_serializer.validated_data:
        user.set_password(user_serializer.validated_data['password'])
    user.save()
    print(44)

    # Update the person instance.
    person.phone = person_serializer.validated_data.get('phone', person.phone)
    person.city = person_serializer.validated_data.get('city', person.city)
    person.email = person_serializer.validated_data.get('email', person.email)
    person.name = person_serializer.validated_data.get('name', person.name)
    person.user = user
    person.save()
    print(55)

    # Serialize and return the updated user and person data.
    serializer_user = SingUpSerializerUser(user, many=False)
    serializer_person = SingUpSerializerPerson(person, many=False)
    print(66)

    return Response({
        'details': 'Your account was modified successfully!',
        'user': serializer_user.data,
        'person': serializer_person.data
    }, status=status.HTTP_200_OK)


User = get_user_model()


class SignUpView(APIView):
    def post(self, request):
        # Split the data into user and person data
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'confirm_password': request.data.get('confirm_password'),
        }

        person_data = {
            'phone': request.data.get('phone'),
            'city': request.data.get('city'),
            'email': request.data.get('email'),
            'name': request.data.get('name'),
        }

        # Validate user data
        user_serializer = SingUpSerializerUser(data=user_data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Validate person data
        person_serializer = SingUpSerializerPerson(data=person_data)
        if not person_serializer.is_valid():
            return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = user_serializer.save()
            person = person_serializer.save(user=user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'User registered successfully',
                'user_id': user.id,
                'person_id': person.id,
                'access': str(refresh.access_token),  # Add access token
                'refresh': str(refresh),  # Add refresh token
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # If anything fails, delete the user if it was created
            if 'user' in locals():
                user.delete()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
