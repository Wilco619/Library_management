import django_tables2 as tables
from .models import Member

class MemberTable(tables.Table):
    export_formats = ['xls', 'xlsx', 'csv']  # a list of formats you'll like to export to
    class Meta:
        model = Member
        fields = ('id','name','regNo','contact')
        # There are more Meta attributes you can use, just look for them in the docs.