from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from . models import Book, Member
from . forms import MemberRegForm, BookRegForm
from django_tables2.views import SingleTableView
from django_tables2.export.views import ExportMixin
from .tables import MemberTable
from django.db.models import Q
import csv

from django.core.paginator import Paginator

# Create your views here.
def login(request):
    
    return render(request, "login.html", locals())

def home(request):
    m_total = Member.objects.count()
    b_count = Book.objects.count()
    return render(request, 'index.html', locals())

def pop(request,popk):
    m_details = get_object_or_404(Member, pk=popk)
    return render(request,"partials/popup.html", locals())

def books(request):

    #set up pagination
    bp = Paginator(Book.objects.all().order_by('title'), 7)
    page = request.GET.get('page')
    book = bp.get_page(page)

    return render(request, "books.html", locals())

def book_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']="attachment; filename=books.csv"

    writer = csv.writer(response)

    books = Book.objects.all().order_by('title')

    writer.writerow(['Book Category', 'Title', 'S_Number', 'Description'])

    for book in books:
        writer.writerow([book.category, book.title, book.s_number, book.description])

    return response

def book_details(request, bpk):
    bk = get_object_or_404(Book,pk=bpk)
    return render(request, 'bookdetails.html', locals())


def member_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=members.csv'

     #create a csv writer
    writer = csv.writer(response)

    #designate the model
    members = Member.objects.all().order_by('name')

    #add column heading to csv file
    writer.writerow(['Member Name', 'Reg Number', 'Contact'])

    #loop through and output
    for member in members:
        writer.writerow([member.name, member.regNo, member.contact])

    return response

def members(request):

    #set up pagination
    p = Paginator(Member.objects.all().order_by('name'), 6)
    page = request.GET.get('page')
    member = p.get_page(page)

    return render(request, "members.html", locals())

def mdetails(request, pk):
    m_details = get_object_or_404(Member, pk=pk)
    return render(request, 'mdetails.html',locals())

def delete_member(request,dpk):
    m_details = get_object_or_404(Member,pk=dpk)
    m_details.delete()
    messages.success(request,"Member Deleted Successfully", extra_tags='alert-success')
    return redirect('members')

def delete_book(request,dbpk):
    book_details = get_object_or_404(Book,pk=dbpk)
    book_details.delete()
    messages.success(request,"Book Deleted Successfully", extra_tags='alert-success')
    return redirect('books')

def update_member(request, upk):
     m_details = get_object_or_404(Member, pk=upk)
     form = MemberRegForm(request.POST or None, instance=m_details)
     if form.is_valid():
        update = Member.objects.get(pk=upk)
        update.name = form.cleaned_data['name']
        update.regNo = form.cleaned_data['regNo']
        update.contact = form.cleaned_data['contact']

        update.save()
        messages.success(request,"Congratulations! Member Updated Successfully", extra_tags='alert-success')
        return redirect('mdetails', pk=upk)
     else:
        messages.warning(request,"Update Member Data!", extra_tags='alert-secondary')
     
     return render(request, 'update-member.html',locals())

def update_book(request, ubpk):
     book_details = get_object_or_404(Book, pk=ubpk)
     form = BookRegForm(request.POST or None, instance=book_details)
     if form.is_valid():
        update = Book.objects.get(pk=ubpk)
        update.category = form.cleaned_data['category']
        update.title = form.cleaned_data['title']
        update.s_number = form.cleaned_data['s_number']
        update.description = form.cleaned_data['description']

        update.save()
        messages.success(request,"Congratulations! Book Updated Successfully", extra_tags='alert-success')
        return redirect('book-details', bpk=ubpk)
     else:
        messages.warning(request,"Update Book Data!", extra_tags='alert-secondary')
     
     return render(request, 'update-book.html',locals())

#memberreg
class MemberView(View):
    def get(self, request):
        mem = 'create'
        form = MemberRegForm()
        return render(request, "memberReg.html", locals())

    def post(self, request):
        mem = 'create'
        form = MemberRegForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            regNo = form.cleaned_data['regNo']
            contact = form.cleaned_data['contact']

            try:
                user = Member.objects.get(regNo=regNo)
                messages.error(request, "Member Already Exists!", extra_tags='alert-danger')
            except Member.DoesNotExist:
                reg = Member(name=name, regNo=regNo, contact=contact)
                reg.save()
                messages.success(request, "Congratulations! Member Saved Successfully.",extra_tags='alert-success')
        else:
            messages.warning(request, "Invalid Data Input", extra_tags='alert-danger')

        return render(request, "memberReg.html", locals())

#bookreg
class BookView(View):
    def get(self, request):
        bk = 'create'
        form = BookRegForm()
        return render(request, "bookReg.html", locals())

    def post(self, request):
        bk = 'create'
        form = BookRegForm(request.POST)
        
        if form.is_valid():
            category = form.cleaned_data['category']
            title = form.cleaned_data['title']
            s_number = form.cleaned_data['s_number']
            description = form.cleaned_data['description']

            try:
                item = Book.objects.get(s_number=s_number)
                messages.error(request, "Book Already Exists!", extra_tags='alert-danger')
            except Book.DoesNotExist:
                reg = Book(category=category, title=title, s_number=s_number, description=description)
                reg.save()
                messages.success(request, "Book Saved Successfully.", extra_tags='alert-success')
        else:
            messages.warning(request, "Invalid Data Input", extra_tags='alert-danger')

        return render(request, "bookReg.html", locals())
    
#for table
class MemberList(ExportMixin, SingleTableView):
    model = Member
    table_class = MemberTable
    export_name = 'All_members'
    template_name = '/members.html'

#searchfield
def search_feature(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        mpost = Member.objects.filter(Q(name__icontains=search_query) | Q(regNo__icontains=search_query))
        return render(request, 'members.html', {'mquery':search_query, 'mpost':mpost})
    else:
        return render(request, 'base.html',{})
    
#booksearch
def search_book(request):
    if request.method == 'POST':
        book_search = request.POST['book_search']
        bpost = Book.objects.filter(Q(title__icontains=book_search) | Q(category__icontains=book_search))
        return render(request, 'books.html', {'bquery':book_search, 'bpost':bpost})
    else:
        return render(request, 'base.html',{})
    
