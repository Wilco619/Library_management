import datetime
from django.db import models

# Create your models here.
    
class Member(models.Model):
    name = models.CharField(max_length=255)
    regNo = models.CharField(max_length=50)
    contact = models.IntegerField(default="")


    def __str__(self):
        return self.name
    

class Book(models.Model):
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    s_number = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    borrower = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL)
    borrow_date = models.DateTimeField('Borrow date', default=datetime.datetime(2023, 9, 15))
    
    def __str__(self):
        return self.title
    