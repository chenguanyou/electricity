#coding=utf-8
import json
from django.http import HttpResponse
from django.views.generic.base import View
from django.core import serializers


from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        '''
        通过Django的View来实现商品的列表页面
        :param request:
        :return:
        '''
        goods = Goods.objects.all()[:10]
        json_disc = serializers.serialize("json", goods)
        json_list = json.loads(json_disc)
        return HttpResponse(json.dumps(json_list), content_type="application/json")


