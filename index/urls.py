from unicodedata import name
from django.urls import path
from .import views
from accounts.views import blog_details, faslname_list, list_of_tags, result_faslname, tag_result , writers , maghalat

urlpatterns = [
    path('home/',views.home_page.as_view(),name="home"),
    path('',views.show_landing,name="landing"),
    # path('?file=<slug:category>/<int:pk>/file')
    path('show/' , views.show_pdf , name='show_pdf'),
    path('show/build/pdf.worker.js/' , views.pdf_work , name='pdfwork'),
    path('show/media/category/computer/' , views.find_pdf , name='findpdf'),
    path('load/<slug:pdfname>' , views.load_pdf , name='loadpdf'),
    path('home/details/<int:pk>/id/<int:id>/' ,blog_details , name='blog_details' ),
    path('home/writers/<int:pk>/' , writers , name="writers"),
    path('home/maghalat/<int:pk>/' , maghalat , name='maghalat'),
    path('home/maghale/download/<int:pk>/' , views.download_pdf , name='download_pdf'),
    path('home/list/tags/<int:id>/' , list_of_tags , name='list_of_tags'),
    path('home/tag/<int:id>/' , tag_result , name="tag_result"),
    path('home/faslname/<int:id>/' , faslname_list , name='faslname'),
    path('home/faslname/result/<int:year>/year/<int:month>/month/<int:category>/category/' , result_faslname , name='result_faslname')

]