from rest_framework import mixins, generics, viewsets
from . import serializers
from ...models import Company, Statement
from .Pagination import ListPagination
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status


class CompanyView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializers.CompanySerializer
    queryset = Company.objects.all()

    pagination_class = ListPagination

    filter_backends = [SearchFilter]
    search_fields = ['symbol', 'name']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StatementView(viewsets.ModelViewSet):
    serializer_class = serializers.StatementSerializer
    pagination_class = ListPagination

    def list(self, request):
        if self.serializer_class.is_valid(self, raise_exception=True):
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response('self.serializer_class.errors', status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        try:
            metric = self.request.query_params.get('metric', '1')

            item_ids_1 = "101"
            item_ids_2_3 = "101, 102"

            if metric == '1':
                sub_sql = "WHERE company_id IN ({company_id}) AND item_id in ({item_id}) AND period IN ({period}) and year>{year_gte} and year<{year_lte}".format(
                    company_id=self.request.query_params.get('company_id'),
                    item_id=item_ids_1,
                    period=self.request.query_params.get('period'),
                    year_gte=int(self.request.query_params.get('year__gte')) - 1,
                    year_lte=int(self.request.query_params.get('year__lte')) + 1,
                )
                sql = "SELECT *,CAST(SUBSTRING (period_end_to_date,1,4) as INTEGER) as year FROM fact_statement {where}".format(where=sub_sql)
            else:
                sub_sql = "WHERE company_id IN ({company_id}) AND item_id in ({item_id}) AND period IN ({period}) and year>{year_gte} and year<{year_lte} ".format(
                    company_id=self.request.query_params.get('company_id'),
                    item_id=item_ids_2_3,
                    period=self.request.query_params.get('period'),
                    year_gte=int(self.request.query_params.get('year__gte')) - 1,
                    year_lte=int(self.request.query_params.get('year__lte')) + 1,
                )
                if metric == '2':
                    sql = "SELECT id,company_id,period,period_end_to_date, SUM (item_value) as item_value,CAST(SUBSTRING (period_end_to_date,1,4) as INTEGER) as year FROM fact_statement {where} GROUP BY company_id, period,period_end_to_date".format(where=sub_sql)
                else:
                    sub_sql = "SELECT *, CAST(SUBSTRING (period_end_to_date,1,4) as INTEGER) as year,CAST(SUBSTRING (period_end_to_date,1,4) as INTEGER)-1 as pyear FROM fact_statement {where}".format(where=sub_sql)
                    sql = "select a.id as id,a.company_id as company_id,a.item_id as item_id,a.period as period,(a.item_value+b.item_value) as item_value from ({subquery}) a INNER JOIN ({subquery}) b ON (a.year-1=b.year AND a.item_id != b.item_id AND a.company_id=b.company_id AND a.period=b.period)".format(subquery=sub_sql)
            return Statement.objects.raw(sql)
        except:
            return None
