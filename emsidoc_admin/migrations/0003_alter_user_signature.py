# Generated by Django 4.2.2 on 2023-07-07 18:32

from django.db import migrations, models
import emsidoc_admin.models


class Migration(migrations.Migration):

    dependencies = [
        ('emsidoc_admin', '0002_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='signature',
            field=models.FileField(upload_to='signatures/', validators=[emsidoc_admin.models.validate_pdf]),
        ),
    ]
