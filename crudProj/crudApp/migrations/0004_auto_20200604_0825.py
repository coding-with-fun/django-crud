# Generated by Django 3.0.6 on 2020-06-04 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudApp', '0003_auto_20200604_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_tags',
            field=models.ManyToManyField(to='crudApp.ProjectTag'),
        ),
    ]