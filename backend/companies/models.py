from django.db import models

# Create your models here.
class Company(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, null=True)
    state = models.IntegerField()

    class Meta:
        db_table = 'dim_company'

    def __str__(self):
        return self.name


class Statement(models.Model):
    item_value = models.BigIntegerField()
    item_id = models.BigIntegerField(null=True)
    unit = models.CharField(max_length=255, default='میلیون ریال')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    period = models.IntegerField()
    period_end_to_date = models.CharField(max_length=255)

    class Meta:
        db_table = 'fact_statement'

    def __str__(self):
        return self.company

    def get_year(self):
        return self.period_end_to_date[0:4]
