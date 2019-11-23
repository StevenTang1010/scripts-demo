from django.shortcuts import render
from datetime import datetime
# from django.http import HttpResponse
# from django.shortcuts import redirect, reverse
from common.models import Types, Goods, Orders, Detail, Users
from django.db.models import Q
from django.core.paginator import Paginator


# 公共信息加载
def loadinfo(request):
    '''公共信息加载'''
    context = {}
    lists = Types.objects.filter(pid=0)
    context['typelist'] = lists
    return context


# 订单信息浏览
def index(request, pIndex=1):
    # 获取订单信息
    mod = Orders.objects
    parmlist = []

    # 获取、判断冰封装keyword关键字搜索
    kw = request.GET.get('keyword', None)
    if kw:
        # 查询收件人和地址中只要含有关键字的都可以
        list = mod.filter(Q(linkman__contains=kw) | Q(address__contains=kw))
        parmlist.append('keyword=' + kw)
    else:
        list = mod.filter()

    # 获取、判断冰封装订单状态state搜索条件
    state = request.GET.get('state', '')
    if state != '':
        list = list.filter(state=state)
        parmlist.append('state=' + state)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 5)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 获取最大页数
    # 判断是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range

    # 遍历订单信息冰追加下订单人姓名信息
    for od in list2:
        user = Users.objects.only('name').get(id=od.uid)
        od.name = user.name

    # 封装信息加载模板输出
    context = {'orderlist': list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages,
               'parmlist': parmlist}
    return render(request, 'myadmin/orders/index.html', context)

# 订单详情信息
def detail(request, oid):
    try:
        # 加载订单信息
        orders = Orders.objects.get(id=oid)
        if orders != None:
            user = Users.objects.only('name').get(id=orders.uid)
            orders.name = user.name

        # 加载订单详情
        dlist = Detail.objects.filter(orderid=oid)
        # 遍历每个商品详情，从Goods中获取对应的图片
        for og in dlist:
            og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname

        # 防止模板变量，加载模板并输出
        context = {'orders': orders, 'detaillist': dlist}
    except Exception as e:
        print(e)
        context = {'info': '没有找到要查看的信息！'}
    return render(request, 'myadmin/orders/index.html', context)

# 修改订单状态
def state(request):
    try:
        oid = request.GET.get('oid', '0')
        ob = Orders.objects.get(id=oid)
        ob.state = request.GET['state']
        ob.save()
        context = {'info':'修改成功！'}
    except Exception as e:
        print(e)
        context = {'info': '修改失败！'}
    return render(request, 'myadmin/info.html', context)
