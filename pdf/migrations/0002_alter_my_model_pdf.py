# Generated by Django 4.0.3 on 2022-03-16 13:54

from django.db import migrations, models
import pdf.models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='my_model',
            name='pdf',
            field=models.FileField(upload_to=pdf.models.local_image_upload_path),
        ),
    ]