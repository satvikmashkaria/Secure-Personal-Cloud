# Generated by Django 2.1.2 on 2018-11-20 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_file_fileinfo_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='upload.FileInfo/bytes/filename/mimetype'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='folder',
            name='parentfolder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='upload.Folder'),
        ),
    ]
