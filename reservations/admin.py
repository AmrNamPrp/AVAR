from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Notifications,ReservationPeriod,Second_Review,RealEstate_Images,NewRealEstate,Review,RealEstate,Extras,Favourits,MyReservations,MyRealEstates,Basics
# Register your models here.

admin.site.register(Review)
admin.site.register(Notifications)
admin.site.register(RealEstate_Images)
admin.site.register(NewRealEstate)
admin.site.register(Extras)
admin.site.register(MyReservations)
admin.site.register(MyRealEstates)
admin.site.register(Favourits)
admin.site.register(Basics)
admin.site.register(Second_Review)
admin.site.register(ReservationPeriod)



# Register your models here.
class RealEstate_admin(admin.ModelAdmin):
    # this will show the products as table
    # name     price      active
    # a         11         T
    # b         10         T
    #  if you turn it to  list_display =['name','active','price']
    # the order of the table will chang
    # name       active        price
    # a            T           10
    # b            T           11


  #   list_editable = ['address',  'price']
    # now you can edit the (active or not) of every product easier
    # you can put      list_editable = ['name','active',...]
    # but you can not put any thing you put in list_display_links
    # which means you can not put 'name' in list_editable , because you put it i in list_display_links
    search_fields = ['town','id', 'latitude', 'longitude', 'city', 'type', 'price']
    # will put box to search among the products based on name
    list_filter = ['city']
    # will create filters based on category and price
    #fields = ['name', 'price', 'category']
    # when you click on the name you will see all information for that products
    # but with this line now you will see just name , price and category

admin.site.register(RealEstate, RealEstate_admin)
# don't forget to do this