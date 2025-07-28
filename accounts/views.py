from unicodedata import category
from django.shortcuts import render ,redirect

from post.models import Magazines , Nashrie , Year , Month , Tags
from .forms import UserRegistrationForm , UserSignUpForm , ProfilePic1 , UpdateProfile , UpdatePasswordProfile , ForgetPassowrd
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login , logout 
from .models import CustomUser , Category
from allauth.account.forms import LoginForm 
from django.contrib import messages
from django.views.generic import ListView , DeleteView , DetailView , CreateView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def login1(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method =="POST":
        form = UserRegistrationForm(request.POST , )

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user1 = authenticate(request,username=username , password=password)
            if user1 is not None:
                login(request,user1)
                return redirect('profile')
            else:
                messages.warning(request,'نام کاربری یا رمز عبور شما اشتباه است')
                form = UserRegistrationForm()
                return render(request,"account/login.html" , {'forms':form})
        else:
            messages.warning(request,'مقادیر را به درستی وارد کنید!')
            form = UserRegistrationForm()
            return render(request,"account/login.html" , {'forms':form})

    else:
        form = UserRegistrationForm()
        return render(request,"account/login.html" , {'forms':form})

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        password_checker = request.POST.get('password')
        if len(password_checker) < 8 :
            form = UserSignUpForm()
            messages.warning(request,'رمز عبور شما بسیار کوتاه است')
            return redirect("signup1")

        if len(request.POST.get('email'))== 0:
            form = UserSignUpForm()
            messages.warning(request,'باید ایمیل را وارد کنید')
            return redirect("signup1")
        if len(request.POST.get('phone_number')) == 0:
            form = UserSignUpForm()
            messages.warning(request,'لطفا شماره تلفن خود را وارد کنید')
            return redirect("signup1")
        if len(request.POST.get('username'))==0:
            form = UserSignUpForm()
            messages.warning(request,'لطفا نام کاربری را وارد کنید')
            return redirect("signup1")
        else:
            username = request.POST.get('username')
            check_user = CustomUser.objects.filter(username=username)
            if check_user == True:
                form = UserSignUpForm()
                messages.warning(request,'این نام کاربری توسط یه کاربر دیگر استفاده شده')
                return redirect("signup1")

        
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            CD = form.cleaned_data
            CustomUser.objects.create(username = CD['username'] , phone_number=CD['phone_number'] , password = make_password(CD['password']) , email=CD['email'])
            messages.success(request,'حساب شما با موفقیت ایجاد شد')
            return redirect("login1")
        else:
            form = UserSignUpForm()
            messages.warning(request,'هر ورودی را به درستی وارد کنید!')
            return redirect("signup1")
            

    else:
        form = UserSignUpForm()
    return render(request,"Sign-up/index.html",{'form':form})

@login_required
def log_out(request):
    if request.method =="POST":
        logout(request)
        return redirect('home')
    else:
        return render(request , 'logout.html')


@login_required
def profile(request):
    if request.method =="POST":
        form = ProfilePic1(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'عکس نمایه شما با موفقیت تغییر کرد')
        else:
            messages.warning(request,'دوباره سعی کنید عکس نمایه خود را آپلود کنید')

        return redirect('profile')
    else:
        form = ProfilePic1()
        return render(request , 'Profile/index.html' , {'form':form})


@login_required
def accept_profiles(request):
    if request.user.roles == "modir":
        user = CustomUser.objects.all().filter(img_accept = False)
        return render (request , 'accept/index.html' , {'users':user})
    else:
        return render(request , '404.html')


@login_required
def approve_profiles(request , pk):
    if request.user.roles == "modir":
        finder = CustomUser.objects.get(id = pk)
        finder.img_accept = True
        finder.save()
        user = CustomUser.objects.all().filter(img_accept = False)
        return render (request , 'accept/index.html' , {'users':user})

    else:
        return render(request , '404.html')

@login_required
def updateprofile(request):
    if request.method == "POST":
        my_user = CustomUser.objects.get(id=request.user.id)
        form = UpdateProfile(request.POST)
        if form.is_valid():
            CD = form.cleaned_data
            if CD['phone_number'] is not None :
                if CD['phone_number'] >= 0:
                    my_user.phone_number = CD['phone_number']
                else:
                    messages.warning(request,'شماره نادرست است')
                    return redirect('profile')
            
            username = CD['username']
            email = CD['email']
            first_name = CD['first_name']
            last_name = CD['last_name']
            if request.user.username != username:
                if len(username)>0:
                    check_user = CustomUser.objects.filter(username=username).exists()
                    if check_user == False :
                        my_user.username = username
                    else:
                        messages.warning(request,'این نام کاربری از قبل وجود دارد')
                        return redirect('profile')

            if request.user.email != email:
                if len(email)>0:
                    check_user = CustomUser.objects.filter(email=email).exists()
                    if check_user == False :
                        my_user.email = email
                    else:
                        messages.warning(request,'این ایمیل وجود دارد !')
                        return redirect('profile')

            if len(first_name) > 0:
                my_user.first_name = first_name
            if len(last_name) > 0:
                my_user.last_name = last_name
            
            CustomUser.save(my_user)
            messages.success(request,'اطلاعات شما با موفقیت تغییر کرد')
            return redirect('profile')
           
        else:
            messages.warning(request,'مطمئن شوید که ورودی ها را به درستی وارد کنید!')
            return redirect('profile')
    else:
        return render(request , 'Profile/index.html')

@login_required
def changepassword(request):
    if request.method == "POST":
        new_pass = request.POST.get('new_pass')
        if len(new_pass)<8:
            messages.warning(request,'رمز عبور شما حداقل باید 8 کاراکتر باشد')
            return redirect('profile')
        else:
            my_user = CustomUser.objects.get(id=request.user.id)
            form = UpdatePasswordProfile(request.POST)
            if form.is_valid():
                CD = form.cleaned_data
                checker = check_password(CD['current_pass'] , my_user.password)
                if checker == True:
                    my_user.password = make_password(CD['new_pass'])
                    CustomUser.save(my_user)
                    messages.success(request,'رمز عبور شما با موفقیت تغییر کرد اکنون دوباره وارد شوید')
                    return redirect ('login1')
                else:
                    messages.warning(request,'رمز عبور شما با رمز عبور حساب شما برابر نیست')
                    return redirect ('profile')
                

    else:
        return render(request , 'Profile/index.html')
    

def passwordforget(request):
    if request.method == "POST":
        form = ForgetPassowrd(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                obj = CustomUser.objects.get(email=email)
                if obj.is_active == False:
                    messages.warning(request,'دسترسی اکانت شما بسته شده است')
                    form = ForgetPassowrd()
                    return render (request , 'registration/password_reset.html' , context={'form':form})

                send_list = []
                send_list.append(obj.email)
            except:
                messages.warning(request,'این ایمیل وجود ندارد')
                form = ForgetPassowrd()
                return render (request , 'registration/password_reset.html' , context={'form':form})

            try:
                send_mail(subject='اطلاعات حساب کاربری' , message=f'با عرض سلام و ادب رمز عبور شما در سایت انجمن علمی کامپیوتر در زیر نوشته شده است \n نا کاربری :\n {obj.username} \nرمز عبور :\n {obj.password}' , from_email=settings.EMAIL_HOST_USER ,recipient_list=send_list)
                return redirect('completereset')
            except:
                messages.warning(request,'ایمیل ارسال نشد')
                form = ForgetPassowrd()
                return render (request , 'registration/password_reset.html' , context={'form':form})

        else:
            messages.warning(request,'ایمیل را درست وارد کنید')
            form = ForgetPassowrd()
            return render (request , 'registration/password_reset.html' , context={'form':form})

            
    else:
        form = ForgetPassowrd()
        return render (request , 'registration/password_reset.html' , context={'form':form})

def completereset(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return render(request , '404.html')

    return render (request , 'registration/password_complete.html')



def blog_details(request , pk , id):



    post = Magazines.objects.get(id = pk)

    final_name = ''
    if post.month.name == "farvardin":
        final_name = "فروردین"
    elif post.month.name == "ordibehesht":
        final_name = "اردیبهشت"
    elif post.month.name == "khordad":
        final_name = "خرداد"
    elif post.month.name == "tir":
        final_name = "تیر"
    elif post.month.name == "mordad":
        final_name = "مرداد"
    elif post.month.name == "shahrivar":
        final_name = "شهریور"
    elif post.month.name == "mehr":
        final_name = "مهر"
    elif post.month.name == "aban":
        final_name = "آبان"
    elif post.month.name == "azar":
        final_name = "آذر"
    elif post.month.name == "dey":
        final_name = "دی"
    elif post.month.name == "bahman":
        final_name = "بهمن"
    elif post.month.name == "esfand":
        final_name= "اسفند"

    posts = ''
    if post.nashrie != None:
        posts = Magazines.objects.all().filter(nashrie=post.nashrie)
    else:
        posts = None
    tags = None
    try:
        tags = Tags.objects.order_by('-views')[:7].filter(category = post.category)
    except:
        try:
            tags = Tags.objects.order_by('-views').filter(category = post.category)
        except:
            pass
    return render(request , "details-blog/news-details.html" , {"magazine":post , "posts":posts , 'tags':tags , "anjoman_id":id , "final_name":final_name})


def writers(request , pk):
    categ = None   
    admins = None

    name = ''
    if pk == 1:
        name = "computer"
    elif pk == 2:
        name = "bargh"
    elif pk == 3:
        name = "pezeshki"
    elif pk == 4:
        name = "mechanic"
    elif pk == 5:
        name = "memari"
    elif pk == 6:
        name = "naft"
    elif pk == 7:
        name = "omran"
    elif pk == 8:
        name = "hoghogh"
    elif pk == 9:
        name= "moshavere"
    elif pk == 10:
        name = "madadkari"
    elif pk == 11:
        name = "havafaza"
    elif pk == 12:
        name = "sanaye"
    elif pk == 13:
        name = "eghtesad"
    elif pk == 14:
        name = "hesabdari"
    elif pk == 15:
        name = "varzesh"
    try:
        categ = Category.objects.get(category=name)
    except:
        pass
    try:
        if categ != None:
            admins = CustomUser.objects.all().filter(category=categ)
    except:
        pass


    return render (request , 'writers/writers.html' , {"anjoman_id":pk , "admins":admins})


def maghalat(request , pk):
    categ = None
    posts = None
    name = ''
    if pk == 1:
        name = "computer"
    elif pk == 2:
        name = "bargh"
    elif pk == 3:
        name = "pezeshki"
    elif pk == 4:
        name = "mechanic"
    elif pk == 5:
        name = "memari"
    elif pk == 6:
        name = "naft"
    elif pk == 7:
        name = "omran"
    elif pk == 8:
        name = "hoghogh"
    elif pk == 9:
        name= "moshavere"
    elif pk == 10:
        name = "madadkari"
    elif pk == 11:
        name = "havafaza"
    elif pk == 12:
        name = "sanaye"
    elif pk == 13:
        name = "eghtesad"
    elif pk == 14:
        name = "hesabdari"
    elif pk == 15:
        name = "varzesh"
    try:
        categ = Category.objects.get(category=name)
    except:
        pass
    try:
        if categ != None:
            posts = Magazines.objects.all().filter(category=categ)
    except:
        pass
    return render(request , 'maghalat/index.html' , {'magazines':posts , "anjoman_id":pk})



def list_of_tags(request , id):

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



    try:
        categ = Category.objects.get(category=name)
        tags= Tags.objects.all().filter(category=categ)
    except:
        tags = None
    
    all_list = []

    if tags != None:
        for i in tags:
            
            tmp_dict = {}
            tmp_dict['tag'] = i.name
            rand_num = random.randint(1 , 9)
            tmp_dict['size'] = rand_num
            tmp_dict['id'] = i.id
            all_list.append(tmp_dict)

    print(all_list)
    return render(request , 'listoftags/index.html' , {'all_tags':all_list , "anjoman_id":id})


def tag_result(request , id):
    try:
        tag= Tags.objects.get(id=id)
        post = Magazines.objects.all().filter(category = tag.category , tags=tag)
    except:
        return render(request , '404.html')
    return render(request , 'tagresult/index.html', {"result":post , 'tag':tag , "anjoman_id":id})




def faslname_list(request , id):

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

    try:
        categ = Category.objects.get(category=name)
        post = Magazines.objects.get(category=categ)
    except:
        tags = None
    
    archive_list = []

    months = Month.objects.all()
    years = Year.objects.all()

    for i in months:
        for j in years:
            checker = Magazines.objects.all().filter(month=i , year = j)
            if checker.exists():
                tmp = {}
                final_name=''
                if i.name == "farvardin":
                    final_name = "فروردین"
                elif i.name == "ordibehesht":
                    final_name = "اردیبهشت"
                elif i.name == "khordad":
                    final_name = "خرداد"
                elif i.name == "tir":
                    final_name = "تیر"
                elif i.name == "mordad":
                    final_name = "مرداد"
                elif i.name == "shahrivar":
                    final_name = "شهریور"
                elif i.name == "mehr":
                    final_name = "مهر"
                elif i.name == "aban":
                    final_name = "آبان"
                elif i.name == "azar":
                    final_name = "آذر"
                elif i.name == "dey":
                    final_name = "دی"
                elif i.name == "bahman":
                    final_name = "بهمن"
                elif i.name == "esfand":
                    final_name= "اسفند"

                tmp['name'] = f'{final_name} {j.name}'
                tmp['year'] = j.id
                tmp['month'] = i.id
                archive_list.append(tmp)
  

    ############## post paginated

    page = request.GET.get('page', 1)

    paginator = Paginator(archive_list, 10)

    all_archive = paginator.page(page)
    page_obj = paginator.get_page(page)
    ###########################################



    return render(request , 'faslname/index.html' , {'archieve':all_archive , "anjoman_id":id , "page_obj":page_obj})



def result_faslname(request , year , month , category):
    name = ''
    if category == 1:
        name = "computer"
    elif category == 2:
        name = "bargh"
    elif category == 3:
        name = "pezeshki"
    elif category == 4:
        name = "mechanic"
    elif category == 5:
        name = "memari"
    elif category == 6:
        name = "naft"
    elif category == 7:
        name = "omran"
    elif category == 8:
        name = "hoghogh"
    elif category == 9:
        name= "moshavere"
    elif category == 10:
        name = "madadkari"
    elif category == 11:
        name = "havafaza"
    elif category == 12:
        name = "sanaye"
    elif category == 13:
        name = "eghtesad"
    elif category == 14:
        name = "hesabdari"
    elif category == 15:
        name = "varzesh"

    try:
        months = Month.objects.get(id=month)
    except:
        return render (request , '404.htmk')
    
    try:
        years = Year.objects.get(id=year)
    except:
        return render(request , '404.html')

    
    try:
        categ = Category.objects.get(category = name)
    except:
        return render(request , '404.html')

    posts = Magazines.objects.all().filter(category=categ , year = years , month=months)

    return render(request , 'faslname_result/index.html' , {'result':posts , 'anjoman_id':category })