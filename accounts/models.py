from django.db import models

# Create your models here.
from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.

class Category(models.Model):
    ROLES = [
        ('pezeshki' , 'مهندسی پزشکی'),
        ('computer' , 'مهندسی کامپیوتر'),
        ('bargh' , 'مهندسی برق'),
        ('mechanic' , 'مهندسی مکانیک'),
        ('memari' , 'مهندسی معماری'),
        ('naft' , "مهندسی نفت"),
        ('omran' , "مهندسی عمران"),
        ('hoghogh' , "حقوق"),
        ('moshavere' , "مشاوره و روانشناسی"),
        ('madadkari' , "مددکاری اجتماعی"),
        ('havafaza' , "مهندسی هوافضا"),
        ('sanaye' , "مهندسی صنایع"),
        ('eghtesad' , "اقتصاد"),
        ('hesabdari' , "حسابداری"),
        ('varzesh' , "تربیت بدنی و علوم ورزشی"),
    ]
    category = models.CharField(max_length=255 , choices=ROLES , verbose_name='دسته بندی')

    def __str__ (self):
        return self.category

class CustomUser(AbstractUser):
    ROLES = [
        ('modir' , 'modir'),
        ('dabir' , 'dabir'),
        ('moaven dabir' , 'moaven dabir'),
        ('khazane dar' , 'khazane dar'),
        ('ozv mamoli' , 'ozv mamoli'),
    ]

    phone_number = models.PositiveIntegerField(null=True , blank=True)
    image = models.ImageField(verbose_name = 'profile' , upload_to ='user/profile/' , blank=True )
    roles = models.CharField(max_length=50 , choices=ROLES , verbose_name='نقش' , blank=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , blank=True , null=True)
    img_accept = models.BooleanField(default=False , blank=True , null=True)
