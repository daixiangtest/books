# Generated by Django 4.2.13 on 2024-06-02 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='图书编号')),
                ('name', models.CharField(max_length=30, verbose_name='图书名称')),
                ('statua', models.BooleanField(default=False, verbose_name='是否出借')),
            ],
            options={
                'verbose_name': '图书表',
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_time', models.DateTimeField(auto_created=True, auto_now=True, verbose_name='还书时间')),
                ('s_time', models.DateTimeField(auto_created=True, verbose_name='出借时间')),
                ('name', models.CharField(max_length=30, verbose_name='借书人')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.books', verbose_name='书籍')),
            ],
            options={
                'verbose_name': '借书记录表',
                'db_table': 'record',
            },
        ),
    ]
