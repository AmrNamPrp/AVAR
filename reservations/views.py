from django.contrib.auth.models import  Group
from .filters import RealEstateFilter
from .serializer import MYRESERVATIONSerializer,Notifications_group_reservationSerializer,Notifications_group_Serializer,Notifications_group_reservationSerializer,Notifications_Serializer,Notifications_reservationSerializer,ReservationPeriodSerializer,NewRealEstateSerializer,RealEstateSerializer,ReviewSerializer,SecondReviewSerializer,FavouritSerializer
from .models import ExpoPushToken,ReservationRejection,Notifications_group,Notifications_reservation_group,Notifications_reservation,Notifications,ReservationPeriod,RealEstate,Review,NewRealEstate,Second_Review,Favourits
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.db.models import Avg
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import RealEstate, Favourits
from rest_framework_simplejwt.authentication import JWTAuthentication  # or your respective auth class
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
User = get_user_model()
import requests
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache
import random
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def gallery(request):
    user = request.user

    # Handle anonymous users safely
    if isinstance(user, AnonymousUser):
        has_unseen = False
    else:
        has_unseen = (
            Notifications_reservation.objects.filter(user_to=user, seen=False).exists() or
            Notifications.objects.filter(user_to=user, seen=False).exists() or
            Notifications_reservation_group.objects.filter(user_to=user, seen=False).exists() or
            Notifications_group.objects.filter(user_to=user, seen=False).exists()
        )

    # Fetch cached order or generate random order for real estates
    cached_order = cache.get("random_real_estate_order")

    if not cached_order:
        real_estate_ids = list(RealEstate.objects.values_list('id', flat=True))
        random.shuffle(real_estate_ids)
        cache.set("random_real_estate_order", real_estate_ids, timeout=600)  # Store for 10 minutes
    else:
        real_estate_ids = cached_order

    filterset = RealEstateFilter(request.GET, queryset=RealEstate.objects.filter(id__in=real_estate_ids))

    serializer = RealEstateSerializer(
        filterset.qs,
        many=True,
        context={'request': request}
    )

    return Response({
        'real estates': serializer.data,
        'has_unseen_notifications': int(has_unseen)
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    user = request.user
    realestat = get_object_or_404(RealEstate, id=pk)
    data = request.data
    review = realestat.review.filter(user=user)

    if data['rating'] <= 0 or data['rating'] > 5:
        return Response({"error": 'Please select between 1 to 5 only'}
                        , status=status.HTTP_400_BAD_REQUEST)
    elif review.exists():
        initial_review = review.first()  # Get the first review for this user
        Second_Review.objects.create(
            user=user,
            real_estate=realestat,
            rating=initial_review.rating,  # Access the rating from the instance
            comment=initial_review.comment  # Access the comment from the instance
        )

        new_review = {'rating': data['rating'], 'comment': data['comment']}
        review.update(**new_review)

        rating = realestat.review.aggregate(avg_ratings=Avg('rating'))
        realestat.ratings = rating['avg_ratings']
        realestat.save()

        return Response({'details': 'realestat review updated'})
    else:
        Review.objects.create(
            user=user,
            real_estate=realestat,
            rating=data['rating'],
            comment=data['comment']
        )
        rating = realestat.review.aggregate(avg_ratings=Avg('rating'))
        realestat.ratings = rating['avg_ratings']
        realestat.save()
        return Response({'details': 'realestat review created'})

@api_view(['GET'])
def res_profile(request, pk):
    realestate = get_object_or_404(RealEstate, id=pk)
    serializer = RealEstateSerializer(realestate, context={'request': request})
    review = realestate.review
    comments = ReviewSerializer(review, many=True)
    secondreview = realestate.second_review
    secondcomments = SecondReviewSerializer(secondreview, many=True)
    return Response({
        'realestate': serializer.data,
        'comments': comments.data,
        'secondcomments': secondcomments.data
    })




@api_view(['GET'])
def comments_of_realestate(request,pk):
    realestate=get_object_or_404(RealEstate,id=pk)
    reviews=realestate.review
    serializer=ReviewSerializer(reviews,many=True)
    return Response({'reviews': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_realestate(request):
    print("1111   ", request.user.username)

    # Check if the user already has a real estate entry
    if NewRealEstate.objects.filter(user=request.user).exists():
        return Response({'details': 'لا يمكنك حجز عقار اخر حتى يتم تأكيد حجزك السابق'}, status=status.HTTP_400_BAD_REQUEST)
    print(232)

    serializer = NewRealEstateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)

        # Create a notification for the creator

        try:
            staff_group = Group.objects.get(name="staff")
            # Send notification to every user in the "staff" group.
            staff_users = staff_group.user_set.all()
            for staff_member in staff_users:
                print(102)
                Notifications_group.objects.create(
                    client=request.user,
                    user_to=staff_member,
                    notification_type='ready_to_assign_add_realestate_admin',
                )

        except Group.DoesNotExist:
            # If the group is not found, you might log it or choose to do nothing.
            pass
        Notifications.objects.create(
            user_to=request.user,
            notification_type='add_realestate_user',
        )
        return Response({'details': 'تم استلام طلبك بنجاح'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favourit_view(request):
    favourites=request.user.favourites
    serializeer=FavouritSerializer(favourites,many=True,        context={'request': request})
    return  Response({'your favourites':serializeer.data})


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def profile(request):
    user = request.user
    person = user.person
    print('user: ',user.username)


    # Filter reservations where the reservationPeriod's status is 'accepted'
    accepted_realestates = ReservationPeriod.objects.filter(status='accepted', user=user).values_list('realestate',flat=True)
    accepted_reservations = RealEstate.objects.filter(id__in=accepted_realestates)
    myrealestates = RealEstate.objects.filter(user=user)
    print(myrealestates)
    serializer_rel = RealEstateSerializer(myrealestates, many=True, context={'request': request})
    serializer_res = MYRESERVATIONSerializer(accepted_reservations, many=True, context={'request': request})
    print(serializer_rel.data)
    return Response({
        'name': person.name,
        'phone': person.phone,
        'city': person.city,
        'username': user.username,
        'your reservations are': serializer_res.data,
        'your real estates are': serializer_rel.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, realestate_id):
    real_estate = get_object_or_404(RealEstate, id=realestate_id)
    favorite_exists = Favourits.objects.filter(
        user=request.user,
        realestate=real_estate
    ).exists()

    if favorite_exists:
        Favourits.objects.filter(
            user=request.user,
            realestate=real_estate
        ).delete()
        return Response({'is_favorite': False}, status=status.HTTP_200_OK)
    else:
        Favourits.objects.create(
            user=request.user,
            realestate=real_estate
        )
        return Response({'is_favorite': True}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_accepted_reservations(request, realestate_id):
    # Filter for reservations with status accepted or DayOff
    reservations = ReservationPeriod.objects.filter(
        realestate_id=realestate_id,
        status__in=['accepted', 'DayOff','pending']
    )
    serializer = ReservationPeriodSerializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_DaysOff_period(request, realestate_id):
    print('DaysOff')
    try:
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the reservation period
        reservation = ReservationPeriod.objects.create(
            user=request.user,
            realestate_id=realestate_id,
            start_date=start_date,
            end_date=end_date,
            status='DayOff'
        )
        # Notifications.objects.create(
        #     user_to=request.user,
        #     describtion='لقد تم بنجاح تحديد تاريخ عطلتك و شكرا لك'
        # )
        serializer = ReservationPeriodSerializer(reservation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def property_bookings(request, realestate_id):
    # Bookings with status "accepted" for current reservations
    accepted_bookings = ReservationPeriod.objects.filter(
        realestate_id=realestate_id, status='accepted'
    )
    # Bookings with status "DayOff" for owner holidays
    dayoff_bookings = ReservationPeriod.objects.filter(
        realestate_id=realestate_id, status='DayOff'
    )

    accepted_serializer = ReservationPeriodSerializer(accepted_bookings, many=True)
    dayoff_serializer = ReservationPeriodSerializer(dayoff_bookings, many=True)

    return Response({
        "accepted_reservations": accepted_serializer.data,
        "dayoff_reservations": dayoff_serializer.data,
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation_period(request, realestate_id):
    try:
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the reservation period with status pending
        reservation = ReservationPeriod.objects.create(
            user=request.user,
            realestate_id=realestate_id,
            start_date=start_date,
            end_date=end_date,
            status='pending'
        )

        # MyReservations.objects.create(
        #     user=request.user,
        #     realestate_id=realestate_id,
        #     reservationPeriod=reservation
        # )


        # Get the default admin user (ensure a user with username 'admin' exists)

        # Create a notification for the creator
        Notifications_reservation.objects.create(
            user_to=request.user,
            notification_type='still_pending_user',
            reservation=reservation
        )
        Notifications_reservation.objects.create(
            user_to=reservation.realestate.user,
            notification_type='res_pending_to_Owner',
            reservation=reservation
        )
        # Send a notification to every user in the designated group (e.g., "reservation_handlers")
        try:
                staff_group = Group.objects.get(name="staff")
                # Send notification to every user in the "staff" group.
                staff_users = staff_group.user_set.all()
                for staff_member in staff_users:
                    print(102)
                    Notifications_reservation_group.objects.create(
                        client=request.user,
                        user_to=staff_member,
                        notification_type='ready_to_assign_reservation_admin',
                        reservation=reservation
                    )
        except Group.DoesNotExist:
            handler_users = []

        # group_message = f"{request.user.username} has asked for a reservation. Would you handle it? (Tap 'assign me')"
        # for user in handler_users:
        #     Notifications_reservation.objects.create(
        #         user_to=user,
        #         describtion=group_message,
        #         notification_type='group_request',
        #         reservation=reservation
        #     )

        serializer = ReservationPeriodSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def assign_reservation(request, reservation_id):
#     """
#     When a handler clicks the "assign me" button from their notification:
#       - Set the current user as the assigned handler.
#       - Remove all group request notifications for this reservation.
#       - Create a new assignment notification for this handler with the options to accept or reject.
#     """
#     try:
#         reservation = ReservationPeriod.objects.get(id=reservation_id)
#
#         if reservation.assigned_handler:
#             return Response({'error': 'This reservation has already been assigned.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         # Ensure that this user belongs to the reservation_handlers group.
#         if not request.user.groups.filter(name='reservation_handlers').exists():
#             return Response({'error': 'You are not authorized to assign this reservation.'},
#                             status=status.HTTP_403_FORBIDDEN)
#
#         admin_user = User.objects.get(username='admin')
#
#         # Set the current user as the handler.
#         reservation.assigned_handler = request.user
#         reservation.save()
#
#         # Remove all group_request notifications for this reservation.
#         Notifications_reservation.objects.filter(
#             reservation=reservation,
#             notification_type='group_request'
#         ).delete()
#
#         # Create a new assignment notification for the handler.
#         Notifications_reservation.objects.create(
#             user_to=request.user,
#             description="The job is yours. Please choose to accept or reject the reservation.",
#             notification_type="assignment",
#             reservation=reservation
#         )
#         return Response({'message': 'Reservation assigned to you.'}, status=status.HTTP_200_OK)
#
#     except ReservationPeriod.DoesNotExist:
#         return Response({'error': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def handle_assignment_action(request, reservation_id):
#     """
#     When the assigned handler chooses to accept or reject:
#       - Update the reservation status accordingly.
#       - Remove the assignment notification.
#       - Notify the original reservation creator with the result.
#     Expect a POST parameter "action" with value "accept" or "reject".
#     """
#     try:
#         action = request.data.get("action")
#         if action not in ["accept", "reject"]:
#             return Response({'error': "Action must be 'accept' or 'reject'."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         reservation = ReservationPeriod.objects.get(id=reservation_id)
#
#         # Verify that the current user is indeed the assigned handler.
#         if reservation.assigned_handler != request.user:
#             return Response({'error': 'You are not assigned to this reservation.'},
#                             status=status.HTTP_403_FORBIDDEN)
#
#         admin_user = User.objects.get(username='admin')
#         if action == "accept":
#             reservation.status = "accepted"
#             result_message = "Your reservation has been accepted."
#         else:  # reject
#             reservation.status = "rejected"
#             result_message = "Your reservation has been rejected."
#
#         reservation.save()
#
#         # Remove the assignment notification that was sent to the handler.
#         Notifications_reservation.objects.filter(
#             reservation=reservation,
#             notification_type="assignment",
#             user_to=request.user
#         ).delete()
#
#         # Notify the creator of the reservation about the result.
#         Notifications_reservation.objects.create(
#             user_to=reservation.user,
#             description=result_message,
#             notification_type="result",
#             reservation=reservation
#         )
#
#         return Response({'message': f"Reservation {action}ed successfully."}, status=status.HTTP_200_OK)
#     except ReservationPeriod.DoesNotExist:
#         return Response({'error': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    # Query all notifications for the authenticated user
    notifications_reservation = Notifications_reservation.objects.filter(user_to=request.user)
    notifications = Notifications.objects.filter(user_to=request.user)
    notifications_reservation_group = Notifications_reservation_group.objects.filter(user_to=request.user)
    notifications_group = Notifications_group.objects.filter(user_to=request.user)

    # Mark all notifications as seen
    notifications_reservation.update(seen=True)
    notifications.update(seen=True)
    notifications_reservation_group.update(seen=True)
    notifications_group.update(seen=True)

    # Serialize each queryset
    serializer1 = Notifications_reservationSerializer(notifications_reservation, many=True)
    serializer2 = Notifications_Serializer(notifications, many=True)
    serializer3 = Notifications_group_reservationSerializer(notifications_reservation_group, many=True)
    serializer4 = Notifications_group_Serializer(notifications_group, many=True)

    # Merge and sort all notifications by creation date in descending order
    all_notifications = list(serializer1.data) + list(serializer2.data) + list(serializer3.data) + list(
        serializer4.data)
    all_notifications.sort(key=lambda x: x['createAt'], reverse=True)

    return Response(all_notifications, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_realestate_notification(request):
    """
    When the user clicks on "تم استلام المهمة" (for a notification of type add_realestate_user),
    this endpoint will:
      - Receive the client id via request.data.
      - Delete all Notifications_group objects having that client.
      - Create a new Notifications_group object with:
         client = old client,
         user_to = currently logged-in user (the one clicking the button),
         notification_type = "got_assigned_add_realestate_admin".
    """
    print(12)
    client_id = request.data.get('client_id')
    if not client_id:
        return Response({"detail": "client_id is required."},
                        status=status.HTTP_400_BAD_REQUEST)


    try:
        print(13)

        client = User.objects.get(id=client_id)
    except User.DoesNotExist:
        return Response({"detail": "Client not found."},
                        status=status.HTTP_404_NOT_FOUND)

    # Remove all notifications in Notifications_group for this client
    print(14)

    Notifications_group.objects.filter(client=client).delete()
    print(15)

    # Create a new notification in Notifications_group with the logged in user as user_to.
    new_notification = Notifications_group.objects.create(
        client=client,  # The old client
        user_to=request.user,  # The user who clicked "تم استلام المهمة"
        notification_type="got_assigned_add_realestate_admin"
    )

    NewRealEstate.objects.filter(user=client).update(assigned_handler=request.user)

    # newRealEstate=NewRealEstate.objects.filter(user=client)
    #
    # print("here:", newRealEstate)
    # print('heere',client)
    # newRealEstate.assigned_handler = request.user
    # newRealEstate.save()
    print(16)

    serializer = Notifications_group_Serializer(new_notification)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_reservation_notification(request):
    """
    This view is called when a staff user clicks on "استلام المهمة" for a notification
    of type "ready_to_assign_reservation_admin." It expects both a client_id and a reservation_id
    in the request. It then:
      - Deletes all Notifications_reservation_group objects matching that client AND reservation.
      - Creates a new Notifications_reservation_group record with:
           client = provided client,
           reservation = provided reservation,
           user_to = the staff member who pressed the button,
           notification_type = "accepting_rejecting_reservation_admin"
    """
    print("assign_reservation_notification: entry")
    client_id = request.data.get('client_id')
    reservation_id = request.data.get('reservation_id')

    if not client_id or not reservation_id:
        return Response({"detail": "client_id and reservation_id are required."},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        client = User.objects.get(id=client_id)
    except User.DoesNotExist:
        return Response({"detail": "Client not found."},
                        status=status.HTTP_404_NOT_FOUND)

    try:
        reservation = ReservationPeriod.objects.get(id=reservation_id)
    except ReservationPeriod.DoesNotExist:
        return Response({"detail": "Reservation not found."},
                        status=status.HTTP_404_NOT_FOUND)

    # Delete all notifications (from staff) for this client/reservation
    print("Deleting notifications for client {} and reservation {}".format(client_id, reservation_id))
    Notifications_reservation_group.objects.filter(client=client, reservation=reservation).delete()

    # Create a new notification for the staff member indicating the assignment has been taken
    new_notification = Notifications_reservation_group.objects.create(
        client=client,
        reservation=reservation,
        user_to=request.user,  # The staff member who clicked the button
        notification_type="accepting_rejecting_reservation_admin"
    )
    ReservationPeriod.objects.filter(id=reservation_id).update(assigned_handler=request.user)
    print("New notification created")
    serializer = Notifications_group_reservationSerializer(new_notification)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_reservation_response(request):
    """
    This endpoint handles a response for a reservation assignment notification.
    Expected JSON parameters:
      - reservation_id: (int) the reservation's id.
      - client_id: (int) the client's id.
      - action: (string) either "accepted" or "rejected".
      - reason: (string, optional) provided when action is "rejected".

    It will update the ReservationPeriod status and the assigned_handler,
    remove waiting notifications, and create a new notification for the staff.
    If rejected, it will also log the rejection reason.
    """
    reservation_id = request.data.get('reservation_id')
    client_id = request.data.get('client_id')
    action = request.data.get('action')
    reason = request.data.get('reason', '')

    if not reservation_id or not client_id or not action:
        return Response(
            {"detail": "reservation_id, client_id, and action are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        reservation = ReservationPeriod.objects.get(id=reservation_id)
    except ReservationPeriod.DoesNotExist:
        return Response({"detail": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        client = User.objects.get(id=client_id)
    except User.DoesNotExist:
        return Response({"detail": "Client not found."}, status=status.HTTP_404_NOT_FOUND)

    # Update the reservation status and assign the handler
    if action == "accepted":
        reservation.status = "accepted"
        Notifications_reservation.objects.create(
            user_to=client,
            notification_type='accepted_user',
            reservation=reservation,
        )
    elif action == "rejected":
        reservation.status = "rejected"
        Notifications_reservation.objects.create(
            user_to=client,
            notification_type='rejected_user',
            reservation=reservation,
        )
    else:
        return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)
    reservation.assigned_handler = request.user
    reservation.save()

    # Remove all notifications of type accepting_rejecting_reservation_admin for this reservation & client.
    Notifications_reservation_group.objects.filter(
        client=client,
        reservation=reservation,
        notification_type="accepting_rejecting_reservation_admin"
    ).delete()

    # Create a new notification depending on the action.
    if action == "accepted":
        new_notification = Notifications_reservation_group.objects.create(
            client=client,
            reservation=reservation,
            user_to=request.user,
            notification_type="accepting_reservation_admin"
        )
        Notifications_reservation.objects.create(
            user_to=reservation.realestate.user,
            notification_type='res_accepted_to_Owner',
            reservation=reservation
        )
    else:  # action is "rejected"
        new_notification = Notifications_reservation_group.objects.create(
            client=client,
            reservation=reservation,
            user_to=request.user,
            notification_type="rejecting_reservation_admin"
        )
        Notifications_reservation.objects.create(
            user_to=reservation.realestate.user,
            notification_type='res_rejected_to_Owner',
            reservation=reservation
        )
        # Save the rejection reason.
        ReservationRejection.objects.create(
            reservation=reservation,
            rejected_by=request.user,
            reason=reason
        )

    serializer = Notifications_group_reservationSerializer(new_notification)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_push_token(request):
    user = request.user
    token = request.data.get('token')
    # احفظ الـ token في قاعدة البيانات
    user.profile.expo_push_token = token
    user.profile.save()
    return Response({'status': 'success'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_expo_token(request):
    token = request.data.get('expo_token')
    if not token:
        return Response({'error': 'Expo token is required'}, status=400)

    ExpoPushToken.objects.update_or_create(
        user=request.user,
        defaults={'token': token}
    )
    return Response({'status': 'success'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification(request):
    user_id = request.data.get('user_id')
    message = request.data.get('message')
    notification_type = request.data.get('type', 'general')

    try:
        device = ExpoPushToken.objects.get(user_id=user_id)
        # استخدم مكتبة requests لإرسال الإشعار
        response = requests.post(
            'https://exp.host/--/api/v2/push/send',
            json={
                'to': device.token,
                'title': 'إشعار جديد',
                'body': message,
                'data': {'type': notification_type}
            }
        )
        return Response(response.json())
    except ExpoPushToken.DoesNotExist:
        return Response({'error': 'User device not found'}, status=404)