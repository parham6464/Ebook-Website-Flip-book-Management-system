from django.urls import path
from .import views
from .views import UpdateProfile, accept_profiles , approve_profiles



urlpatterns = [
    path('login/',views.login1 , name='login1'),
    # path('sign-up/',views.sign_up , name='signup1'),
    path('logout/' , views.log_out , name='logout1'),
    path('profile/' ,views.profile, name='profile'),
    path('profile/update/' , views.updateprofile , name='updateprofile'),
    path('profile/changepassword/' , views.changepassword , name='changepassword'),
    path('login/forgetpassword/' , views.passwordforget , name='passwordforget'),
    path('login/complete/' , views.completereset , name='completereset'),
    path ('profile/accept/image/' , accept_profiles , name='accept_profile'),
    path ('profile/accept/image/<int:pk>/' , approve_profiles , name='approve_profiles'),
    
    
]