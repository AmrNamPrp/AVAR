from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Person(models.Model):
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
        ('رقه', 'رقه'),
        ('الحسكة', 'الحسكة'),
        ('اللاذقية', 'اللاذقية'),
        ('طرطوس', 'طرطوس'),
    )
    phone=models.CharField(max_length=30,default="")
    city=models.CharField(max_length=30,null=True,choices=cities)
    user=models.OneToOneField(User,verbose_name='user',null=True,on_delete=models.CASCADE,related_name='person')
    email=models.EmailField(null=True,blank=True)
    name=models.CharField(max_length=30,default="")
    note=models.TextField(default='')
    def __str__(self):
        return self.name