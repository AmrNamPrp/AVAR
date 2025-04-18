from rest_framework import serializers
from .models import ReservationPeriod,RealEstate_Images,Extras,Basics,RealEstate, Review, NewRealEstate, Second_Review, Favourits, MyReservations, MyRealEstates
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # add more if needed

class RealEstateImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstate_Images
        fields = ['image']  # You can add more fields if necessary.


class BasicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basics
        fields = ['describtion', 'photo']

class ExtrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extras
        fields = ['describtion', 'photo']


class RealEstateSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    basics = BasicsSerializer(many=True, read_only=True)  # For "المعلومات الاساسية"
    extras = ExtrasSerializer(many=True, read_only=True)  # For "المعلومات الإضافية"
    images = RealEstateImagesSerializer(many=True, read_only=True)  # For additional images

    class Meta:
        model = RealEstate
        fields = [
            'id', 'price', 'city', 'town', 'type',
            'max_members', 'rooms', 'bathrooms',
            'pool', 'period', 'ratings', 'photo',
            'is_favorite', 'basics', 'extras', 'images',
            'latitude', 'longitude'
        ]

    def get_is_favorite(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            is_favorite = obj.favourites_list.filter(user=request.user).exists()
            i = 0
            i = i + 1
            print('realestate: ',obj.id,' the user', request.user, 'is_favorite:', is_favorite)
            return is_favorite
        return False


class NewRealEstateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewRealEstate
        fields = "__all__"
        read_only_fields = ('user',)


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Review
        fields = "__all__"

class SecondReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Second_Review
        fields = "__all__"

class FavouritSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favourits
        fields="__all__"



class MyReservationsSerializer(serializers.ModelSerializer):
    # Nest the RealEstateSerializer for detailed information
    realestate = RealEstateSerializer(read_only=True)

    class Meta:
        model = MyReservations
        fields = '__all__'

class ReservationPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationPeriod
        fields = '__all__'

class MyRealEstatesSerializer(serializers.ModelSerializer):
    # Nest the RealEstateSerializer for detailed information
    realestate = RealEstateSerializer(read_only=True)

    class Meta:
        model = MyRealEstates
        fields = '__all__'



class ReservationPeriodSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = ReservationPeriod
        # Include any additional fields you want to return
        fields = ['id', 'user_name', 'user_phone', 'start_date', 'end_date', 'status']