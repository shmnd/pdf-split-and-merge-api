# Generated by Django 5.0.4 on 2024-04-28 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_pdf_files_alter_students_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pdf_Files',
        ),
    ]
