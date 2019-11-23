from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from common.models import Users, Types, Goods, Orders, Detail
from ..forms import ResetPwdForm
from django.core.paginator import Paginator


# 公共信息加载函数
def loadinfo(request):
    list = Types.objects.filter(pid=0)
    context = {'typelist': list}
    return context


# 浏览会员个人中心订单信息
def viporders(request, state=None):
    context = loadinfo(request)
    if state == 0:
        # 获取当前登陆者的订单信息
        odlist = Orders.objects.filter(uid=request.session['vipuser']['id']).filter(state=state)
        # 遍历订单信息，查询对那个的详情信息
        for od in odlist:
            delist = Detail.objects.filter(orderid=od.id)
            # 遍历订单详情，并且获取对应的商品图片信息
            for og in delist:
                og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname
            od.detaillist = delist
    elif state == 1:
        # 获取当前登陆者的订单信息
        odlist = Orders.objects.filter(uid=request.session['vipuser']['id']).filter(state=state)
        # 遍历订单信息，查询对那个的详情信息
        for od in odlist:
            delist = Detail.objects.filter(orderid=od.id)
            # 遍历订单详情，并且获取对应的商品图片信息
            for og in delist:
                og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname
            od.detaillist = delist
    elif state == 2:
        # 获取当前登陆者的订单信息
        odlist = Orders.objects.filter(uid=request.session['vipuser']['id']).filter(state=state)
        # 遍历订单信息，查询对那个的详情信息
        for od in odlist:
            delist = Detail.objects.filter(orderid=od.id)
            # 遍历订单详情，并且获取对应的商品图片信息
            for og in delist:
                og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname
            od.detaillist = delist
    elif state == 3:
        # 获取当前登陆者的订单信息
        odlist = Orders.objects.filter(uid=request.session['vipuser']['id']).filter(state=state)
        # 遍历订单信息，查询对那个的详情信息
        for od in odlist:
            delist = Detail.objects.filter(orderid=od.id)
            # 遍历订单详情，并且获取对应的商品图片信息
            for og in delist:
                og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname
            od.detaillist = delist
    else:
        # 获取当前登陆者的订单信息
        odlist = Orders.objects.filter(uid=request.session['vipuser']['id'])
        # 遍历订单信息，查询对那个的详情信息
        for od in odlist:
            delist = Detail.objects.filter(orderid=od.id)
            # 遍历订单详情，并且获取对应的商品图片信息
            for og in delist:
                og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname
            od.detaillist = delist
    context['orderslist'] = odlist
    return render(request, 'myweb/viporders.html', context)


# 修改订单状态
def odstate(request):
    try:
        oid = request.GET.get('oid', 0)
        ob = Orders.objects.get(id=oid)
        ob.state = request.GET['state']
        ob.save()
        return redirect(reverse('vip_orders'))
    except Exception as e:
        print(e)
        return HttpResponse('订单处理失败！')


# # 浏览会员个人中心订单信息
# def viporders(request):
#     pass
# # 浏览会员个人中心订单信息
# def viporders(request):
#     pass

# 浏览会员信息
def info(request):
    user = Users.objects.get(id=request.session['vipuser']['id'])
    context = {'user': user}
    return render(request, 'myweb/vipinfo.html', context)


# 修改会员信息
def update(request):
    try:
        user = Users.objects.get(id=request.session['vipuser']['id'])
        user.sex = request.POST['sex']
        user.address = request.POST['address']
        user.code = request.POST['code']
        user.phone = request.POST['phone']
        user.email = request.POST['email']
        user.save()
        context = {'info': '修改成功'}
    except Exception as e:
        print(e)
        context = {'info': '修改失败'}
    return render(request, 'myweb/info.html', context)


# 重置会员密码
def resetps(request):
    user = Users.objects.get(id=request.session['vipuser']['id'])
    context = {'user': user}
    return render(request, 'myweb/reset.html', context)


# 执行重置会员密码
def doresetps(request):
    try:
        user = Users.objects.get(id=request.session['vipuser']['id'])
        import hashlib
        m = hashlib.md5()
        m.update(bytes(request.POST['password'], encoding='utf8'))
        user.password = m.hexdigest()
        user.save()
        context = {'info': '修改成功'}
    except Exception as e:
        print(e)
        context = {'info': '修改失败'}
    return render(request, 'myweb/info.html', context)
