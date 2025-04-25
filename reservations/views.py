from django.contrib.auth.models import User, Group
from .filters import RealEstateFilter
from .serializer import Notifications_Serializer,Notifications_reservationSerializer,ReservationPeriodSerializer,NewRealEstateSerializer,RealEstateSerializer,ReviewSerializer,SecondReviewSerializer,FavouritSerializer,MyRealEstatesSerializer,MyReservationsSerializer
from .models import Notifications_reservation,Notifications,MyReservations,ReservationPeriod,RealEstate,Review,NewRealEstate,Second_Review,Favourits
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



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def gallery(request):
    user=request.user

    filterset = RealEstateFilter(request.GET, queryset=RealEstate.objects.all())
    print(11)
    #print(user.person.name)
    serializer = RealEstateSerializer(
        filterset.qs,
        many=True,
        context={'request': request}
    )
    print(2)
    result = {'real estates': serializer.data}
    return Response(result)


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

    serializer = NewRealEstateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        message = 'لقد تم استلام طلبك بنجاح ,سنتواصل معك على رقمك حتى نضيف عقارك ,شكرا لوثوقك بنا'

        # Create a notification for the creator
        Notifications.objects.create(
            user_to=request.user,
            describtion=message,
            notification_type='self',
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
    # Filter reservations where the reservationPeriod's status is 'accepted'
    accepted_reservations = user.reservations.filter(reservationPeriod__status='accepted')
    myrealestates = user.myrealestates

    serializer_rel = MyRealEstatesSerializer(myrealestates, many=True, context={'request': request})
    serializer_res = MyReservationsSerializer(accepted_reservations, many=True, context={'request': request})

    return Response({
        'name': person.name,
        'phone': person.phone,
        'email': person.email,
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
    print('1111111111111111111   ')
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

# -------------------------------
# Existing views (gallery, create_review, res_profile, comments_of_realestate,
# new_realestate, favourit_view, profile, toggle_favorite, etc.)
# (Leave them as you had.)


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
        MyReservations.objects.create(
            user=request.user,
            realestate_id=realestate_id,
            reservationPeriod=reservation
        )

        # Get the default admin user (ensure a user with username 'admin' exists)
        admin_user = User.objects.get(username='admin')
        user_message='لقد قمت بحجز العقار بنجاح,قم بتثبيت الحجز عن طريق دفع الدفعة الاولى من المبلغ ,او سيتم الغاء الحجز بعد 24 ساعة من الان'

        # Create a notification for the creator
        Notifications_reservation.objects.create(
            user_to=request.user,
            describtion=user_message,
            notification_type='self',
            reservation=reservation
        )

        # Send a notification to every user in the designated group (e.g., "reservation_handlers")
        try:
            handlers_group = Group.objects.get(name='reservation_handlers')
            handler_users = handlers_group.user_set.all()
        except Group.DoesNotExist:
            handler_users = []

        group_message = f"{request.user.username} has asked for a reservation. Would you handle it? (Tap 'assign me')"
        for user in handler_users:
            Notifications_reservation.objects.create(
                user_to=user,
                describtion=group_message,
                notification_type='group_request',
                reservation=reservation
            )

        serializer = ReservationPeriodSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_reservation(request, reservation_id):
    """
    When a handler clicks the "assign me" button from their notification:
      - Set the current user as the assigned handler.
      - Remove all group request notifications for this reservation.
      - Create a new assignment notification for this handler with the options to accept or reject.
    """
    try:
        reservation = ReservationPeriod.objects.get(id=reservation_id)

        if reservation.assigned_handler:
            return Response({'error': 'This reservation has already been assigned.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Ensure that this user belongs to the reservation_handlers group.
        if not request.user.groups.filter(name='reservation_handlers').exists():
            return Response({'error': 'You are not authorized to assign this reservation.'},
                            status=status.HTTP_403_FORBIDDEN)

        admin_user = User.objects.get(username='admin')

        # Set the current user as the handler.
        reservation.assigned_handler = request.user
        reservation.save()

        # Remove all group_request notifications for this reservation.
        Notifications_reservation.objects.filter(
            reservation=reservation,
            notification_type='group_request'
        ).delete()

        # Create a new assignment notification for the handler.
        Notifications_reservation.objects.create(
            user_to=request.user,
            describtion="The job is yours. Please choose to accept or reject the reservation.",
            notification_type="assignment",
            reservation=reservation
        )
        return Response({'message': 'Reservation assigned to you.'}, status=status.HTTP_200_OK)

    except ReservationPeriod.DoesNotExist:
        return Response({'error': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_assignment_action(request, reservation_id):
    """
    When the assigned handler chooses to accept or reject:
      - Update the reservation status accordingly.
      - Remove the assignment notification.
      - Notify the original reservation creator with the result.
    Expect a POST parameter "action" with value "accept" or "reject".
    """
    try:
        action = request.data.get("action")
        if action not in ["accept", "reject"]:
            return Response({'error': "Action must be 'accept' or 'reject'."},
                            status=status.HTTP_400_BAD_REQUEST)

        reservation = ReservationPeriod.objects.get(id=reservation_id)

        # Verify that the current user is indeed the assigned handler.
        if reservation.assigned_handler != request.user:
            return Response({'error': 'You are not assigned to this reservation.'},
                            status=status.HTTP_403_FORBIDDEN)

        admin_user = User.objects.get(username='admin')
        if action == "accept":
            reservation.status = "accepted"
            result_message = "Your reservation has been accepted."
        else:  # reject
            reservation.status = "rejected"
            result_message = "Your reservation has been rejected."

        reservation.save()

        # Remove the assignment notification that was sent to the handler.
        Notifications_reservation.objects.filter(
            reservation=reservation,
            notification_type="assignment",
            user_to=request.user
        ).delete()

        # Notify the creator of the reservation about the result.
        Notifications_reservation.objects.create(
            user_to=reservation.user,
            describtion=result_message,
            notification_type="result",
            reservation=reservation
        )

        return Response({'message': f"Reservation {action}ed successfully."}, status=status.HTTP_200_OK)
    except ReservationPeriod.DoesNotExist:
        return Response({'error': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    notifications_reservation = Notifications_reservation.objects.filter(user_to=request.user)
    notifications = Notifications.objects.filter(user_to=request.user)

    serializer1 = Notifications_reservationSerializer(notifications_reservation, many=True)
    serializer2 = Notifications_Serializer(notifications, many=True)
    all_notifications = list(serializer1.data) + list(serializer2.data)
    all_notifications.sort(key=lambda x: x['createAt'], reverse=True)  # Sort in descending order (newest first)
    return Response(all_notifications)