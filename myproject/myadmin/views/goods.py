from django.shortcuts import render
from django.http import HttpResponse
from common.models import Goods, Types
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import redirect
import time, os
from PIL import Image
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request, pageindex):
    '''浏览信息'''
    goods = Goods.objects

    # 获取数据对象
    parmlist = []
    # print(list)
    username = request.GET.get('goods')
    if username:
        list = goods.filter(Q(goods__contains=goods))
        parmlist.append('goods=' + goods)
    else:
        list = goods.all().order_by('id')
        # print(list)
    typeid = request.GET.get('typeid', '')
    if typeid != '':
        list = list.filter(typeid=typeid)
        parmlist.append('typeid=' + typeid)

    # 遍历商品信息，并获取对应的商品类别名称，并以typename名封装
    for vo in list:
        ty = Types.objects.get(id=vo.typeid)
        vo.typename = ty.name
    if not pageindex:
        pageindex = 1
    # print(pageindex)
    p = Paginator(list, 5)  # 分页，每页数量10
    goodslist = p.page(pageindex)  # 保存分页后的会员列表
    plist = p.page_range  # 保存页码列表
    context = {'goodslist': goodslist, 'pagelist': plist, 'pagecount': len(plist), 'pageindex': pageindex,
               'parmlist': parmlist}
    return render(request, 'myadmin/goods/index.html', context)


def add(request):
    '''加载添加页面'''
    # 获取商品类别信息
    tlist = Types.objects.extra(select={'_has': 'concat(path,id)'}).order_by('_has')
    for bo in tlist:
        bo.pname = '....' * (bo.path.count(',') - 1)
    context = {'typelist': tlist}
    return render(request, 'myadmin/goods/add.html', context)


@csrf_exempt
def insert(request):
    '''执行图片的上传'''
    try:
        myfile = request.FILES.get("pic", None)
        if not myfile:
            return HttpResponse("没有上传文件信息")
        filename = str(time.time()) + '.' + myfile.name.split('.').pop()
        filepath = os.path.join('./static/pics/' + filename)
        # print("./static/photos/" + str(filename))
        with open(filepath, "wb+") as destination:
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)

        # 执行图片缩放
        im = Image.open(filepath)
        # 缩放到375*375(缩放后的宽高比例不变):
        im.thumbnail((375, 375))
        # 把缩放后的图像用jpeg格式保存:filepath
        im.save(filepath, None)
        # 缩放到75*75(缩放后的宽高比例不变):
        im.thumbnail((75, 75))
        im.save("./static/pics/s_" + filename, None)
        # 缩放到220*220(缩放后的宽高比例不变):
        im.thumbnail((220, 220))
        im.save("./static/pics/m_" + filename, None)

        # 保存商品信息
        ob = Goods()
        ob.goods = request.POST['goods']
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        ob.content = request.POST['content']
        ob.picname = filename
        ob.state = 1
        ob.addtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': '添加成功'}

    except Exception as e:
        print(e)
        context = {'info': '添加失败'}
    return render(request, 'myadmin/info.html', context)


# def insert(request):
#     '''执行添加'''
#     try:
#         ob = Goods()
#         ob.name = request.POST['name']
#         ob.pid = request.POST['pid']
#         ob.path = request.POST['path']
#         ob.save()
#         context = {'info': '添加成功'}
#     except Exception as e:
#         print(e)
#         context = {'info': '添加失败'}
#     return render(request, 'myadmin/info.html', context)

def delete(request, gid):
    '''删除信息'''
    try:
        obj = Goods.objects.get(id=gid)
        if obj.state == 1:
            if os.path.exists('static/pics' + obj.picname):
                os.remove('static/pics/' + obj.picname)
            else:
                print('1')
            if os.path.exists('static/pics/s_' + obj.picname):
                os.remove('static/pics/s_' + obj.picname)
            if os.path.exists('static/pics/m_' + obj.picname):
                os.remove('static/pics/m_' + obj.picname)
            obj.delete()
            context = {'info': '删除成功'}
        else:
            context = {'info': '该商品不是新商品，不允许删除'}
    except Exception as e:
        print(e)
        context = {'info': '删除失败'}
    return render(request, 'myadmin/info.html', context)


def edit(request, gid):
    '''加载编辑页面'''
    try:
        # print(uid)
        ob = Goods.objects.get(id=gid)
        ty = Types.objects.get(id=ob.typeid)
        ob.typename = ty.name
        tlist = Types.objects.extra(select={'id': 'id', '_has': 'concat(path,id)'}).order_by('_has')
        for bo in tlist:
            bo.pname = '....' * (bo.path.count(',') - 1)
        context = {'Goods': ob, 'typelist': tlist}
        return render(request, 'myadmin/goods/edit.html', context)
    except Exception as e:
        print(e)
        context = {'info': '没有找到要修改的信息'}
    return render(request, 'myadmin/info.html', context)


def update(request, gid):
    '''执行图片的上传'''
    try:
        myfile = request.FILES.get("pic", None)
        if myfile:  # 判断是否上传图片
            # 如果上传了新的图片，那么先删除原来的图片
            obj = Goods.objects.get(id=gid)
            if os.path.exists('static/pics' + obj.picname):
                os.remove('static/pics/' + obj.picname)
            else:
                pass
            if os.path.exists('static/pics/s_' + obj.picname):
                os.remove('static/pics/s_' + obj.picname)
            else:
                pass
            if os.path.exists('static/pics/m_' + obj.picname):
                os.remove('static/pics/m_' + obj.picname)
            else:
                pass
            filename = str(time.time()) + '.' + myfile.name.split('.').pop()  # 拼接图片的时间
            filepath = os.path.join('./static/pics/' + filename)
            # print("./static/photos/" + str(filename))
            with open(filepath, "wb+") as destination:
                for chunk in myfile.chunks():  # 分块写入文件
                    destination.write(chunk)
            # 执行图片缩放
            im = Image.open(filepath)
            # 缩放到375*375(缩放后的宽高比例不变):
            im.thumbnail((375, 375))
            # 把缩放后的图像用jpeg格式保存:filepath
            im.save(filepath, None)
            # 缩放到75*75(缩放后的宽高比例不变):
            im.thumbnail((75, 75))
            im.save("./static/pics/s_" + filename, None)
            # 缩放到220*220(缩放后的宽高比例不变):
            im.thumbnail((220, 220))
            im.save("./static/pics/m_" + filename, None)
            # 保存商品信息
            obj.goods = request.POST['goods']
            obj.typeid = request.POST['typeid']
            obj.company = request.POST['company']
            obj.price = request.POST['price']
            obj.store = request.POST['store']
            obj.content = request.POST['content']
            obj.state = request.POST['state']
            obj.picname = filename
            obj.save()
            context = {'info': '修改成功'}
        else:  # 如果未上传图片，则修改其他字段信息
            # 保存商品信息
            obj = Goods.objects.get(id=gid)
            obj.goods = request.POST['goods']
            obj.typeid = request.POST['typeid']
            obj.company = request.POST['company']
            obj.price = request.POST['price']
            obj.store = request.POST['store']
            obj.content = request.POST['content']
            obj.state = request.POST['state']
            obj.save()
            context = {'info': '修改成功'}

    except Exception as e:
        print(e)
        context = {'info': '修改失败'}
    return render(request, 'myadmin/info.html', context)
