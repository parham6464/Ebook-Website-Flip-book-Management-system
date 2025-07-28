from unicodedata import category
from django.shortcuts import render , redirect
from .forms import NewMagazineForm 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustomUser
from django.views import generic
from .models import Magazines , Year , Month , Category
from django.contrib.auth.mixins import LoginRequiredMixin
import jdatetime
from datetime import datetime


# Create your views here.
@login_required
def add_magazine(request):
    sss=jdatetime
    fa_date =sss.datetime.now().strftime("%m")
    real_month =''
    if fa_date == '01':
        real_month='farvardin'
    elif fa_date == "02":
        real_month = "ordibehesht"
    elif fa_date == "03":
        real_month = "khordad"
    elif fa_date == "04":
        real_month = "tir"
    elif fa_date == "05":
        real_month = "mordad"
    elif fa_date == "06":
        real_month = "shahrivar"
    elif fa_date == "07":
        real_month = "mehr"
    elif fa_date == "08":
        real_month = "aban"
    elif fa_date == "09":
        real_month = "azar"
    elif fa_date == "10":
        real_month = "dey"
    elif fa_date == "11":
        real_month = "bahman"
    elif fa_date == "12":
        real_month = "esfand"
    
    year_checker = sss.datetime.now().strftime("%Y")
    obj_year = None
    obj_month = None
    try :
        obj_year=Year.objects.get(name=year_checker)
    except:
        obj_year=Year.objects.create(name=year_checker)

    try:
        obj_month=Month.objects.get(name=real_month)
    except:
        pass

    if request.method == "POST":
        forms = NewMagazineForm(request.POST , request.FILES)
        if forms.is_valid():
            obj= forms.save(commit=False)
            if obj.category != request.user.category:
                if request.user.roles !="modir":
                    messages.warning(request , 'فقط مدیر می تواند در انجمن های دیگر پست بگذارد شما فقط مجاز به گذاشتن پست در انجمن خود هستید')
                    forms = NewMagazineForm()
                    return render(request , 'addmagazine/books_new.html' , context={'forms':forms})

            obj.user = request.user
            obj.nevisandeh = request.user.username
            obj.year = obj_year
            obj.month = obj_month

            if request.user.roles =="modir" or request.user.roles == "dabir":
                obj.published = True
                messages.success(request,'پست شما منتشر شد')
            else:
                messages.success(request,'پست شما پس از تایید مدیر یا دبیر انجمن منتشر می شود')
            obj.save()

            forms = NewMagazineForm()
            return render(request , 'addmagazine/books_new.html' , context={'forms':forms})
        else:
            messages.warning(request,'اطلاعات را درست وارد نکرده اید')
            forms = NewMagazineForm()
            return render(request , 'addmagazine/books_new.html' , context={'forms':forms})
    else:
        forms = NewMagazineForm()
        return render(request , 'addmagazine/books_new.html' , context={'forms':forms})
    




class myposts(generic.ListView , LoginRequiredMixin):
    model = CustomUser
    # paginate_by = 5
    template_name = 'myposts/myposts.html'
    context_object_name = 'me'

@login_required
def editposts(request , pk):
    if request.method =="POST":
        try:
            obj = Magazines.objects.get(pk=pk  , user=request.user)
        except:
            return render(request , '404.html')
        forms = NewMagazineForm(request.POST,request.FILES,instance=obj)
        if forms.is_valid():
            forms.save()
            return render(request , 'editmagazine/books_new.html' , context={'obj':obj , "forms":forms})
        else:
            messages.warning(request,'اطلاعات را درست وارد نکرده اید')
            obj = Magazines.objects.get(pk=pk)
            forms = NewMagazineForm(instance=obj)
            return render(request , 'editmagazine/books_new.html' , context={'obj':obj , "forms":forms})
    
    else:
        try:
            obj = Magazines.objects.get(pk=pk , user=request.user)
            forms = NewMagazineForm(instance=obj)
            return render(request , 'editmagazine/books_new.html' , context={'obj':obj , "forms":forms})
        except:
            return render(request , '404.html')

@login_required
def deletemagazine(request , pk):
    role = request.user.roles
    if role =='dabir':

        if request.method == "POST":
            try:
                obj = Magazines.objects.get(pk=pk , user=request.user , category=request.user.category)
            except:
                return render(request , '404.html')
            obj.delete()
            return redirect ('myposts')
        else:
            return render(request , 'acceptdelete.html')
    elif role == "modir":
        if request.method == "POST":
            try:
                obj = Magazines.objects.get(pk=pk , user=request.user)
            except:
                return render(request , '404.html')
            obj.delete()
            return redirect ('myposts')
        else:
            return render(request , 'acceptdelete.html')

    else:
        return render(request , '404.html')

@login_required
def allposts(request):
    role = request.user.roles
    if role =='dabir':
        allusers = CustomUser.objects.all().filter(category=request.user.category)
        obj = Magazines.objects.all().filter(category=request.user.category)
        return render (request , 'allposts/myposts.html' , {'magazines':obj , 'allusers':allusers})
    elif role == 'modir':
        allusers = CustomUser.objects.all()
        obj = Magazines.objects.all()
        return render (request , 'allposts/myposts.html' , {'magazines':obj , 'allusers':allusers})

    else:
        return render(request , '404.html')

    

@login_required
def allpostsfilter(request , pk):
    role = request.user.roles
    if role =='dabir':
        allusers = CustomUser.objects.all().filter(category=request.user.category)
        try:
            user1 = CustomUser.objects.get(pk=pk , category=request.user.category)
        except:
            return render(request , '404.html')

        obj = Magazines.objects.all().filter(user=user1)
        return render (request , 'allposts/myposts.html' , {'magazines':obj , 'allusers':allusers})
    elif role == "modir":
        allusers = CustomUser.objects.all()
        try:
            user1 = CustomUser.objects.get(pk=pk)
        except:
            return render(request , '404.html')

        obj = Magazines.objects.all().filter(user=user1)
        return render (request , 'allposts/myposts.html' , {'magazines':obj , 'allusers':allusers})

    else:
        return render(request , '404.html')


@login_required
def allowposts(request):
    role = request.user.roles
    if role =='dabir':

        allusers = CustomUser.objects.all().filter(category=request.user.category)
        obj = Magazines.objects.all().filter(category=request.user.category)
        return render (request , 'allowposts/myposts.html' , {'magazines':obj , 'allusers':allusers})
    elif role == "modir":

        allusers = CustomUser.objects.all()
        obj = Magazines.objects.all()
        return render (request , 'allowposts/myposts.html' , {'magazines':obj , 'allusers':allusers})

    else:
        return render(request , '404.html')


@login_required
def allowpostfilter(request , pk):
    role = request.user.roles
    if role =='dabir':
        try:
            allusers = CustomUser.objects.all().filter(category=request.user.category)
            user1 = CustomUser.objects.get(pk=pk , category=request.user.category)
            obj = Magazines.objects.all().filter(user=user1)
        except:
            return render(request , '404.html')
        return render (request , 'allowposts/myposts.html' , {'magazines':obj , 'allusers':allusers})
    elif role == "modir":
        try:
            allusers = CustomUser.objects.all()
            user1 = CustomUser.objects.get(pk=pk )
            obj = Magazines.objects.all().filter(user=user1)
        except:
            return render(request , '404.html')
        return render (request , 'allowposts/myposts.html' , {'magazines':obj , 'allusers':allusers})

    else:
        return render(request , '404.html')

@login_required
def publishpost(request , pk):
    role = request.user.roles
    if role == "modir" or role =='dabir':

        if request.method =="POST":
            obj = Magazines.objects.get(pk=pk)
            print(obj.id)
            forms = NewMagazineForm(request.POST,request.FILES,instance=obj)
            if forms.is_valid():
                obj1=forms.save(commit=False)
                obj1.published=True
                obj1.save()
                messages.success(request,'پست منتشر شد')
                return render(request , 'editpostallow/books_new.html' , context={'obj':obj , "forms":forms})
            else:
                messages.warning(request,'اطلاعات را درست وارد نکرده اید')
                obj = Magazines.objects.get(pk=pk)
                forms = NewMagazineForm(instance=obj)
                return render(request , 'editpostallow/books_new.html' , context={'obj':obj , "forms":forms})
        
        else:

            obj = Magazines.objects.get(pk=pk)
            forms = NewMagazineForm(instance=obj)
            return render(request , 'editpostallow/books_new.html' , context={'obj':obj , "forms":forms})
    else:
        return render(request , '404.html')


def searchname(request , id):

    categ = None
    posts = None
    name = ''
    if id == 1:
        name = "computer"
    elif id == 2:
        name = "bargh"
    elif id == 3:
        name = "pezeshki"
    elif id == 4:
        name = "mechanic"
    elif id == 5:
        name = "memari"
    elif id == 6:
        name = "naft"
    elif id == 7:
        name = "omran"
    elif id == 8:
        name = "hoghogh"
    elif id == 9:
        name= "moshavere"
    elif id == 10:
        name = "madadkari"
    elif id == 11:
        name = "havafaza"
    elif id == 12:
        name = "sanaye"
    elif id == 13:
        name = "eghtesad"
    elif id == 14:
        name = "hesabdari"
    elif id == 15:
        name = "varzesh"

    categ = Category.objects.get(category=name)

    search_name=request.POST.get('q')
    if search_name == None:
        return redirect('home')

    obj = Magazines.objects.all().filter(category=categ)

    tmp = []
    for i in obj:
        if search_name in i.title_name:
            tmp.append(i.id)
    
    obj1 = Magazines.objects.all().filter(id__in=tmp)
    return render(request , 'homesearch/index.html' , context={'result':obj1 , 'anjoman_id':id})
    