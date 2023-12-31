# Generated by Django 4.2.2 on 2023-07-08 17:32

import ckeditor.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('address', models.CharField(max_length=50, null=True)),
                ('phone', models.CharField(max_length=10, null=True)),
                ('role', models.IntegerField(choices=[(1, 'Customer'), (2, 'Employee'), (3, 'Admin')], default=1)),
                ('avatar', models.ImageField(null=True, upload_to='users/%Y/%m')),
                ('accumulatePoint', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('subTotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BillDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.bill')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EvenDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discountPrice', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ImportBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', ckeditor.fields.RichTextField(null=True)),
                ('unitPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unitsInStock', models.IntegerField()),
                ('image', models.ImageField(null=True, upload_to='sales/%Y/%m')),
                ('bills', models.ManyToManyField(related_name='products', through='sales.BillDetail', to='sales.bill')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.category')),
            ],
        ),
        migrations.CreateModel(
            name='ImportDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.ImageField(upload_to='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('importBill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.importbill')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.product')),
            ],
        ),
        migrations.AddField(
            model_name='importbill',
            name='products',
            field=models.ManyToManyField(related_name='imports', through='sales.ImportDetail', to='sales.product'),
        ),
        migrations.AddField(
            model_name='importbill',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.supplier'),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('endDate', models.DateTimeField(auto_now_add=True)),
                ('product', models.ManyToManyField(related_name='events', through='sales.EvenDetail', to='sales.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='evendetail',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.event'),
        ),
        migrations.AddField(
            model_name='evendetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.product'),
        ),
        migrations.AddField(
            model_name='billdetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.product'),
        ),
    ]
