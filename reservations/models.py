from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE, PROTECT


class Extras(models.Model):
    describtion=models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photo/Extras', null=True, blank=True)
    def __str__(self):
        return self.describtion



class Basics(models.Model):
    describtion=models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photo/Extras', null=True, blank=True)
    def __str__(self):
        return self.describtion



class RealEstate(models.Model):

    types = (
        ('مزرعة', 'مزرعة'),
        ('فيلّا', 'فيلّا'),
        ('شقة', 'شقة'),

    )
    cities = (
        ('خارج سوريا', 'خارج سوريا'),
        ('ادلب', 'ادلب'),
        ('دمشق', 'دمشق'),
        ('حلب', 'حلب'),
        ('ريف دمشق', 'ريف دمشق'),
        ('حماه', 'حماه'),
        ('حمص', 'حمص'),
        ('درعا', 'درعا'),
        ('القنيطرة', 'القنيطرة'),
        ('السويداء', 'السويداء'),
        ('دير الزور', 'دير الزور'),
        ('القامشلي', 'القامشلي'),
        ('الحسكة', 'الحسكة'),
        ('اللاذقية', 'اللاذقية'),
        ('طرطوس', 'طرطوس'),
    )
    periods = (
        ('بالليلة', 'بالليلة'),
        ('بالشهر', 'بالشهر'),
    )
    TorF=(
        ('Yes','Yes'),
        ('No','No')

    )
    basics=models.ManyToManyField(Basics)
    extras=models.ManyToManyField(Extras)
    price = models.DecimalField(decimal_places=2,null=True, max_digits=10, verbose_name='السعر')
    city=models.CharField(max_length=30,null=True,choices=cities,verbose_name='المحافظة')
    town=models.CharField(max_length=30,default="",verbose_name='المنطقة')
    type=models.CharField(max_length=30,null=True,choices=types,verbose_name='نوع العقار')
    max_members=models.IntegerField(default=0,verbose_name='عدد الاشخاص المسموح')
    rooms=models.IntegerField(default=0,verbose_name='عدد الغرف')
    bathrooms=models.IntegerField(default=0,verbose_name='عدد الحمامات')
    pool=models.CharField(max_length=10,null=True,choices=TorF,verbose_name='هل يوجد مسبح؟')
    period=models.CharField(max_length=30,null=True,choices=periods,verbose_name='باليوم او بالشهر؟')
    ratings = models.DecimalField(max_digits=3,decimal_places=2,default=0)
    photo = models.ImageField(upload_to='photo/properties', null=True, blank=True)
    describtion=models.TextField(default='')
    latitude = models.FloatField(null=True, blank=True, verbose_name='خط العرض')
    longitude = models.FloatField(null=True, blank=True, verbose_name='خط الطول')


    def __str__(self):
        return self.town


class RealEstate_Images(models.Model):
    image=models.ImageField(upload_to='photos/properties',blank=True,null=True,verbose_name='الصورة')
    realestate=models.ForeignKey(RealEstate,null=True,on_delete=models.CASCADE,related_name='images')

class Review(models.Model):
    real_estate = models.ForeignKey(RealEstate,null=True,blank=False,on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000, default="", blank=False)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Second_Review(models.Model):
    real_estate = models.ForeignKey(RealEstate,null=True,blank=False,on_delete=models.CASCADE, related_name='second_review')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000, default="", blank=False)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class ReservationPeriod(models.Model):

    status=(
       ('pending','pending'),
       ('rejected','rejected'),
       ('accepted','accepted'),
       ('DayOff','DayOff'),

    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservation_periods'
    )
    realestate = models.ForeignKey(
        RealEstate,
        on_delete=models.CASCADE,
        related_name='reservation_periods'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(default='',max_length=30,choices=status)

    def __str__(self):
        return f"{self.realestate} reserved from {self.start_date} to {self.end_date}"


class NewRealEstate(models.Model):
    types = (
        ('مزرعة', 'مزرعة'),
        ('فيلّا', 'فيلّا'),
        ('شقة', 'شقة'),

    )
    address_choices = (
        ('خارج سوريا', 'خارج سوريا'),
        ('ادلب', 'ادلب'),
        ('دمشق', 'دمشق'),
        ('حلب', 'حلب'),
        ('ريف دمشق', 'ريف دمشق'),
        ('حماه', 'حماه'),
        ('حمص', 'حمص'),
        ('درعا', 'درعا'),
        ('القنيطرة', 'القنيطرة'),
        ('السويداء', 'السويداء'),
        ('دير الزور', 'دير الزور'),
        ('القامشلي', 'القامشلي'),
        ('الحسكة', 'الحسكة'),
        ('اللاذقية', 'اللاذقية'),
        ('طرطوس', 'طرطوس'),
    )
    city = models.CharField(max_length=30, blank=True, null=True, choices=address_choices, verbose_name='المحافظة')
    town = models.CharField(max_length=30, blank=True, null=True, verbose_name='المدينة او البلدة')
    type=models.CharField(max_length=30,blank=True,null=True,choices=types,verbose_name='نوع العقار')
    notes=models.CharField(max_length=500,blank=True,null=True,verbose_name='ملاحظات')
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username



class Favourits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='الزبون', related_name='favourites')
    realestate = models.ForeignKey(RealEstate, on_delete=models.CASCADE,verbose_name='العقار', related_name='favourites_list')

    def __str__(self):
        return self.user.username


class MyReservations(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='صاحب العقار', related_name='reservations')
    realestate = models.ForeignKey(RealEstate, on_delete=models.CASCADE,verbose_name='العقار', related_name='reservation_list')
    reservationPeriod=models.ForeignKey(ReservationPeriod,null=True,on_delete=CASCADE)

    def __str__(self):
        return self.user.username


class MyRealEstates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='صاحب العقار', related_name='myrealestates')
    realestate = models.OneToOneField(RealEstate, on_delete=models.CASCADE,verbose_name='العقار', related_name='myrealestates_list')
    def __str__(self):
        return self.user.username


class Notifications(models.Model):
    user_from=models.ForeignKey(User,null=True,on_delete=PROTECT,related_name='user_from')
    user_to=models.ForeignKey(User,null=True,default='',on_delete=CASCADE,related_name='user_to')
    describtion=models.TextField(default='')
