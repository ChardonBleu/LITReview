# Generated by Django 3.2.5 on 2021-08-30 15:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0012_auto_20210826_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='headline',
            field=models.CharField(help_text="The headline can't be blank. Headline max length 128.", max_length=128),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], help_text='Each review has rating wich is an integer number between            0 and 5.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='ticket',
            field=models.ForeignKey(help_text='Each review is related to Ticket describing a book or an            article.If the related ticket is deleted, the review is deleted.', on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='library.ticket'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(help_text='', on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(help_text='Each ticket has a title wich is book title and author', max_length=128),
        ),
        migrations.AlterField(
            model_name='userfollows',
            name='followed_user',
            field=models.ForeignKey(help_text='', on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userfollows',
            name='user',
            field=models.ForeignKey(help_text='', on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
