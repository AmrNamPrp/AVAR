from .filters import RealEstateFilter
from .serializer import ReservationPeriodSerializer,NewRealEstateSerializer,RealEstateSerializer,ReviewSerializer,SecondReviewSerializer,FavouritSerializer,MyRealEstatesSerializer,MyReservationsSerializer
from .models import ReservationPeriod,RealEstate,Review,NewRealEstate,Second_Review,Favourits
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.db.models import Avg
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from django.core.cache import cache
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
    # Include the user's id in the cache key if they are authenticated; otherwise, use 'anon'

    filterset = RealEstateFilter(request.GET, queryset=RealEstate.objects.all())
    print(1)
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
    serializer = NewRealEstateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
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
    user=request.user
    person=user.person
    reservations=user.reservations
    myrealestates=user.myrealestates
    serializer_rel=MyRealEstatesSerializer(myrealestates,many=True,context={'request': request})
    serializer_res=MyReservationsSerializer(reservations,many=True,context={'request': request})
    return Response({
                    'name':person.name,
                    'phone':person.phone,
                    'email':person.email,
                    'city':person.city,
                    'username':user.username,
                     'your reservations are':serializer_res.data,
                     'your real estates are':serializer_rel.data
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

        # Create the reservation period
        reservation = ReservationPeriod.objects.create(
            user=request.user,
            realestate_id=realestate_id,
            start_date=start_date,
            end_date=end_date,
            status='pending'
        )
        print("reservation")
        serializer = ReservationPeriodSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_accepted_reservations(request, realestate_id):
    # Filter for reservations with status accepted or DayOff
    reservations = ReservationPeriod.objects.filter(
        realestate_id=realestate_id,
        status__in=['accepted', 'DayOff']
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