# Generated by Django 4.2.3 on 2023-08-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_member_rename_books_book_delete_members_member_books'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='status',
        ),
        migrations.AlterField(
            model_name='book',
            name='s_number',
            field=models.CharField(max_length=100),
        ),
    ]
