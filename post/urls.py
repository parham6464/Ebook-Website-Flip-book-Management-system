from django.urls import path
from .import views
from .views import *



urlpatterns = [
    path('addmagazine/', views.add_magazine , name='addmagazine'),
    path('myposts/' , views.myposts.as_view() , name='myposts'),
    path('editmagazine/<int:pk>/' ,  views.editposts , name='editposts'),
    path('deletemagazine/<int:pk>/' ,  views.deletemagazine , name='deletemagazine'),
    path('allposts/' ,  views.allposts , name='allposts'),
    path('allposts/<int:pk>/' ,  views.allpostsfilter , name='allpostsfilter'),
    path('allowposts/' , views.allowposts , name='allowposts'),
    path('allowposts/<int:pk>/' , views.allowpostfilter , name='allowpostsfilter'),
    path('publishpost/<int:pk>/' , views.publishpost , name='publishpost'),
    path('home/search/result/<int:id>/' , views.searchname , name='searchname'),

]