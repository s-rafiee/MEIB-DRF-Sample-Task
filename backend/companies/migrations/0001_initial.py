# Generated by Django 4.1 on 2022-08-10 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('industry', models.CharField(max_length=255, null=True)),
                ('state', models.IntegerField()),
            ],
            options={
                'db_table': 'dim_company',
            },
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_value', models.BigIntegerField()),
                ('item_id', models.BigIntegerField(null=True)),
                ('unit', models.CharField(default='میلیون ریال', max_length=255)),
                ('period', models.IntegerField()),
                ('period_end_to_date', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company')),
            ],
            options={
                'db_table': 'fact_statement',
            },
        ),
    ]
