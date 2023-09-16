from django.contrib import admin
from . models import Book, Member

# Register your models here.
@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display=['id','category','title','s_number','description']

@admin.register(Member)
class MemberModelAdmin(admin.ModelAdmin):
    list_display=['id','name','regNo','contact']


