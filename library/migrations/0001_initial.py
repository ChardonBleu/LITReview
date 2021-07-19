# Generated by Django 3.2.5 on 2021-07-19 13:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Each ticket has a title wich is the book title and author', max_length=128)),
                ('description', models.TextField(blank=True, help_text='Each ticket has a description.            It can describe the book and-or can request for information            on this book.', max_length=2048)),
                ('image', models.ImageField(blank=True, help_text='Each ticket can have an image. It can be blank.', null=True, upload_to='')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, help_text='ticket creation date is automatically filled in.')),
                ('user', models.ForeignKey(help_text='Each ticket has been created by one user.            If the user is deleted, the ticket is deleted.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime_created',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(help_text='Each review has a rating wich is an integer number between 0 and 5.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('headline', models.CharField(help_text="The headline can't be blank. Headline max length is 128.", max_length=128)),
                ('body', models.CharField(blank=True, help_text='The body can be blank. Body max length is 8192.', max_length=8192)),
                ('datetime_created', models.DateTimeField(auto_now_add=True, help_text='Each review is related tu a user. If the user is deleted,            the review is deleted.')),
                ('ticket', models.ForeignKey(help_text='Each review is related to a Ticket describing a book or an article.            If a the related ticket is deleted, the review is deleted.', on_delete=django.db.models.deletion.CASCADE, to='library.ticket')),
                ('user', models.ForeignKey(help_text='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-datetime_created',),
            },
        ),
        migrations.CreateModel(
            name='UserFollows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_user', models.ForeignKey(help_text='', on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(help_text='', on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'followed_user')},
            },
        ),
    ]
