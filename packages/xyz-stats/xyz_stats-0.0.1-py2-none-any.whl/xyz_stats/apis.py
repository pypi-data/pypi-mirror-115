# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals

from . import models, serializers
from rest_framework import viewsets, decorators, response
from xyz_restful.decorators import register


@register()
class MeasureViewSet(viewsets.ModelViewSet):
    queryset = models.Measure.objects.all()
    serializer_class = serializers.MeasureSerializer
    search_fields = ('name', 'code', 'description')
    filter_fields = {
        'id': ['in', 'exact'],
        'name': ['exact'],
        'content_type': ['exact'],
        'is_active': ['exact'],
        'create_time': ['exact'],
    }


@register()
class ReportViewSet(viewsets.ModelViewSet):
    queryset = models.Report.objects.all()
    serializer_class = serializers.ReportSerializer
    search_fields = ('name', 'description')
    filter_fields = {
        'id': ['in', 'exact'],
        'name': ['exact'],
        'is_active': ['exact'],
        'create_time': ['exact'],
    }

    @decorators.action(['GET'], detail=True)
    def daily(self, request, pk):
        report = self.get_object()
        qps = request.query_params
        ds = report.daily_query(begin_date=qps.get('begin_date'), end_date=qps.get('end_date'))
        return response.Response(dict(data=ds, fields=report.get_table_fields()))


@register()
class ReportMeasureViewSet(viewsets.ModelViewSet):
    queryset = models.ReportMeasure.objects.all()
    serializer_class = serializers.ReportMeasureSerializer
    search_fields = ('name',)
    filter_fields = {
        'id': ['in', 'exact'],
        'report': ['exact'],
        'measure': ['exact']
    }
