import re
from django.shortcuts import render , redirect
from django.http import HttpResponse
from post.models import Magazines
from django.views import generic
from django.urls import resolve   
from django.http import FileResponse

# Create your views here.

class home_page(generic.ListView):
    model = Magazines
    paginate_by = 6
    template_name = 'Home/index.html'
    context_object_name = 'magazines'

# def home_page(request):
#     return render(request,"Home/index.html")

def load_pdf(request , pdfname):
    if "127.0" in request.build_absolute_uri():
        print('222222222222222')
    print(request.build_absolute_uri())
    request.session['pdfname'] = pdfname
    return redirect("http://127.0.0.1:8000/show/?file=media/category/computer/&magazineMode=true")


def show_landing(request):
    return render(request , "landing/landing.html")

def show_pdf(request ):
    
    return render (request , "flipbook/viewer.html")

def pdf_work(request):
    test_file = open('./index/static/flipbook/script/pdf.worker.js', 'rb')
    response = HttpResponse(content=test_file)
    response['Content-Type'] = 'application/javascript'
    return response

def find_pdf(request ):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return render(request , '404.html')

    pdfname = request.session.get('pdfname')
    obj = Magazines.objects.all().filter(id=pdfname)
    for i in obj:
        file_name = i.pdf.name.split('/')[-1]
    test_file = open(f'./media/category/computer/{file_name}', 'rb')
    response = HttpResponse(content=test_file)
    response['Content-Type'] = 'application/pdf'
    return response


    
def download_pdf(request , pk):
    post = Magazines.objects.get(id=pk)
    return FileResponse(post.pdf, content_type='application/pdf',as_attachment=True)
