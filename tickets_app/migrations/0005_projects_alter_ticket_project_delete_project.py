# Generated by Django 4.0.3 on 2022-04-08 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets_app', '0004_alter_project_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('FE', 'FRONT-END'), ('BE', 'BACK-END'), ('IO', 'IOS'), ('AN', 'ANDROID')], max_length=15)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('contributors', models.ManyToManyField(related_name='contributing', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='ticket',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='tickets_app.projects'),
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]