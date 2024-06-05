import time

from django.db import transaction
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.views import View
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from .models import *


# Create your views here.

# 登录接口
class LoginView(View):
    # 退出登录
    def get(self, request):
        logout(request)
        return JsonResponse({'code': 200, 'message': '退出登录成功'})

    # 登录页面
    def post(self, request):
        data = request.POST
        # 获取请求的数据
        params = request.POST if len(data) > 0 else json.loads(request.body.decode())
        user = authenticate(request=request, username=params['user'], password=params['passwd'])
        if user is not None:
            login(request, user)
            return JsonResponse({'code': 200, 'message': '登录成功'})
        else:
            return JsonResponse({'code': 201, 'message': '登录失败'})


class BooksView(View):
    # 查询图书
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'code': 201, 'message': '没有登录'})
        book = Books.objects.all()
        data = []
        for i in book:
            item = dict(id=i.id, name=i.name, statua=i.statua)
            data.append(item)
        return JsonResponse({'code': 200, 'message': 'success', 'data': data})

    # 增加图书
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'code': 201, 'message': '没有登录'})
        params = request.POST if len(request.POST) > 0 else json.loads(request.body.decode())
        if params['id'] and params['name'] is None:
            return JsonResponse({'code': 202, 'message': '字段填写完整'})
        try:
            Books.objects.get(id=params['id'])
            return JsonResponse({'code': 203, 'message': '字段重复'})
        except Exception as e:
            Books.objects.create(id=params['id'], name=params['name'])
        return JsonResponse({'code': 200, 'message': '添加成功'})

    # 删除书籍
    def delete(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'code': 201, 'message': '没有登录'})
        params = request.GET
        try:
            params['id']
        except Exception as e:
            return JsonResponse({'code': 203, 'message': '请输入id字段'})
        try:
            book = Books.objects.get(id=params['id'])
            book.delete()
            return JsonResponse({'code': 200, 'message': '删除成功'})
        except Exception as e:
            return JsonResponse({'code': 202, 'message': '删除失败图书不存在'})


class LendView(View):
    ids = 0

    # 借书接口
    def post(self, request):
        # 判断是否登录
        if not request.user.is_authenticated:
            return JsonResponse({'code': 201, 'message': '没有登录'})
        # 查询书籍是否存在
        params = request.POST if len(request.POST) > 0 else json.loads(request.body.decode())

        try:
            book = Books.objects.get(id=params['book'])
            if book.statua:
                return JsonResponse({'code': 203, 'message': '这本书已经出借了'})
        except Exception as e:
            return JsonResponse({'code': 202, 'message': '没有这本书'})
        else:
            with transaction.atomic():
                book.statua = True
                book.save()
                a = Record.objects.create(book=book, name=params['name'])
                id = a.id
                return JsonResponse({'code': 200, 'message': '书籍出借成功', "id": id})

    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'code': 201, 'message': '没有登录'})
        params = request.GET
        try:
            book = Books.objects.get(id=params['id'])
        except Exception as e:
            return JsonResponse({'code': 202, 'message': '没有这本书'})
        if not book.statua:
            return JsonResponse({'code': 203, 'message': '这本书没有出借'})
        else:
            with transaction.atomic():
                book.statua = False
                book.save()
                print(self.ids)
                record = Record.objects.get(id=params['ids'])
                # record = Record.objects.create(book=book, name=params['name'])
                record.s_time = datetime.now()
                record.save()
                return JsonResponse({'code': 200, 'message': '还书成功'})
