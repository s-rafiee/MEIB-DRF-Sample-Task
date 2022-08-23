from rest_framework import serializers
from ...models import Company, Statement
from rest_framework.exceptions import ValidationError


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'symbol', 'name', 'industry', 'state']


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ['item_id', 'item_value', 'company', 'period', 'period_end_to_date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if request.query_params.get('metric') == '2':
            rep['item_id'] = 5000
        elif request.query_params.get('metric') == '3':
            rep['item_id'] = 6000
        return rep

    def is_valid(self, raise_exception=False):
        # Parameters
        metric = self.request.query_params.get('metric', None)
        period = self.request.query_params.get('period', '').split(',')
        company_id = self.request.query_params.get('company_id', '').split(',')
        year__lte = self.request.query_params.get('year__lte', None)
        year__gte = self.request.query_params.get('year__gte', None)

        # Metric Validate.
        try:
            if not (int(metric) >= 1 and int(metric) <= 3):
                raise ValidationError('metric is invalid.')
        except:
            raise ValidationError('metric is invalid.')

        # Period Validate.
        try:
            period = [int(p) for p in period]
        except:
            raise ValidationError('period is invalid.')

        # company_id Validate.
        try:
            company_id = [int(p) for p in company_id]
        except:
            raise ValidationError('company_id is invalid.')

        # year__lte Validate.
        try:
            year__lte = int(year__lte)
        except:
            raise ValidationError('year__lte is invalid.')

        # year__gte Validate.
        try:
            year__gte = int(year__gte)
            if year__gte > year__lte:
                raise ValidationError('year__gte must be smaller than year__lte.')
        except:
            raise ValidationError('year__gte is invalid.')
        return True
