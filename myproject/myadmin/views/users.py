from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users
from django.core.paginator import Paginator
import hashlib
from django.db.models import Q


# Create your views here.
def index(request, pageindex):
    '''浏览信息'''
    users = Users.objects  # 获取数据对象
    parmlist = []
    # print(list)
    username = request.GET.get('username')
    if username:
        list = users.filter(Q(username__contains=username) | Q(name__contains=username))
        parmlist.append('username='+username)
    else:
        list = users.all().order_by('id')
        # print(list)
    sex = request.GET.get('sex', '')
    if sex != '':
        list = list.filter(sex=sex)
        parmlist.append('sex='+sex)
    if not pageindex:
        pageindex = 1
    # print(pageindex)
    p = Paginator(list, 7)  # 分页，每页数量10
    userlist = p.page(pageindex)  # 保存分页后的会员列表
    plist = p.page_range  # 保存页码列表
    context = {'userslist': userlist, 'pagelist': plist, 'pagecount': len(plist), 'pageindex': pageindex,
               'parmlist': parmlist}
    return render(request, 'myadmin/users/index.html', context)


def add(request):
    '''加载添加页面'''
    return render(request, 'myadmin/users/add.html')


def insert(request):
    '''执行添加'''
    try:
        ob = Users()
        ob.username = request.POST['username']
        ob.name = request.POST['name']
        # 获取密码并md5
        m = hashlib.md5()
        m.update(bytes(request.POST['password'], encoding='utf8'))
        ob.password = m.hexdigest()
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = 1
        ob.save()
        context = {'info': '添加成功'}
    except Exception as e:
        print(e)
        context = {'info': '添加失败'}
    return render(request, 'myadmin/info.html', context)


def delete(request, uid):
    '''删除信息'''
    try:
        Users.objects.filter(id=uid).delete()
        context = {'info': '删除成功'}
    except Exception as e:
        print(e)
        context = {'info': '删除失败'}
    return render(request, 'myadmin/info.html', context)


def edit(request, uid):
    '''加载编辑页面'''
    try:
        # print(uid)
        ob = Users.objects.get(id=uid)
        context = {'users': ob}
        return render(request, 'myadmin/users/edit.html', context)
    except Exception as e:
        print(e)
        context = {'info': '没有找到要修改的信息'}
    return render(request, 'myadmin/info.html', context)


def update(request, uid):
    '''执行信息编辑'''
    try:
        user = Users.objects.get(id=uid)
        # print(user)
        user.name = request.POST['name']
        user.sex = request.POST['sex']
        user.address = request.POST['address']
        user.code = request.POST['code']
        user.phone = request.POST['phone']
        user.email = request.POST['email']
        user.state = request.POST['state']
        user.save()
        context = {'info': '修改成功'}

    except Exception as e:
        print(e)
        context = {'info': '修改失败'}

    return render(request, 'myadmin/info.html', context)


def reset(request, uid):
    '''加载编辑页面'''
    try:
        # print(uid)
        ob = Users.objects.get(id=uid)
        context = {'user': ob}
        return render(request, 'myadmin/users/reset.html', context)
    except Exception as e:
        print(e)
        context = {'info': '没有找到要修改的信息'}
    return render(request, 'myadmin/info.html', context)


def do_reset(request, uid):
    '''重置用户密码'''
    try:
        user = Users.objects.get(id=uid)
        # 获取密码并md5
        m = hashlib.md5()
        m.update(bytes(request.POST['password'], encoding='utf8'))
        user.password = m.hexdigest()
        user.save()
        context = {'info': '修改成功'}

    except Exception as e:
        print(e)
        context = {'info': '修改失败'}

    return render(request, 'myadmin/info.html', context)
