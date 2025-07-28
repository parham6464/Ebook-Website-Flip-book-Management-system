from unicodedata import category
from django.db import models
from accounts.models import CustomUser , Category
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget 
from ckeditor.fields import RichTextField

# Create your models here.

class Year (models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Month(models.Model):
    OPTIONS = [
        ('farvardin' , 'فروردین'),
        ('ordibehesht' , 'اردیبهشت'),
        ('khordad' , 'خرداد'),
        ('tir' , 'تیر'),
        ('mordad' , 'مرداد'),
        ('shahrivar' , 'شهریور'),
        ('mehr' , 'مهر'),
        ('aban' , 'آبان'),
        ('azar' , 'آذر'),
        ('dey' , 'دی'),
        ('bahman' , 'بهمن'),
        ('esfand' , 'اسفند'),
    ]

    name = models.CharField(max_length=255 , choices=OPTIONS)

    def __str__ (self):
        return self.name

class Nashrie(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , null=True , blank=True)

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , null=True , blank=True)

    def __str__(self):
        return self.name

class Magazines(models.Model):

    def validate_file_extension(value):
        try:
            if value.file.content_type != 'application/pdf':
                raise ValidationError(u'Error message')
        except:
            return True

    title_name = models.CharField(max_length=250 , verbose_name='موضوع مجله')
    title_picture = models.ImageField(upload_to='category/pictures/' , verbose_name='عکس مجله')
    tozihat = RichTextField(default=None,null=True , blank=True , verbose_name='توضیحات')
    pdf = models.FileField(upload_to='category/computer/' , verbose_name='فایل پی دی اف' , validators=[validate_file_extension])
    user = models.ForeignKey(CustomUser , on_delete=models.SET_NULL , related_name='magazines' , verbose_name='کاربر' , null=True , blank=True)
    nevisandeh = models.CharField(max_length=100 , null=True , blank=True)

    published = models.BooleanField(default=False , verbose_name='انتشار' , blank=True)
    date_create = models.DateTimeField(auto_now_add=True)   
    category = models.ForeignKey(Category , on_delete=models.CASCADE , null=True , verbose_name='انجمن' )
    tags = models.ForeignKey(Tags , on_delete=models.CASCADE , null=True , default=None , blank=True  , verbose_name='تگ')
    nashrie = models.ForeignKey(Nashrie , on_delete=models.CASCADE , null=True , blank=True , verbose_name='نشریه')

    saheb_emtiaz = models.CharField(max_length=255 , blank=True , null=True  , verbose_name='صاحب امتیاز')
    modir_masol = models.CharField(max_length=255 , blank=True , null=True , verbose_name='مدیر مسئول')
    sar_dabir = models.CharField(max_length=255 , blank=True , null=True , verbose_name='سر دبیر')

    month = models.ForeignKey(Month , on_delete=models.CASCADE , null=True , blank=True)
    year = models.ForeignKey(Year , on_delete=models.CASCADE, null=True , blank=True)

    def __str__(self):
        return self.title_name

