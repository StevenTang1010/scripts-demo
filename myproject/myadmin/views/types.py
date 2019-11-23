from django.shortcuts import render
from django.http import HttpResponse
from common.models import Types


# Create your views here.
def index(request):
    '''浏览信息'''
    list = Types.objects.extra(select={'_has': 'concat(path,id)'}).order_by('_has')
    # 遍历查询结果，添加一个类别缩进效果属性
    for ob in list:
        ob.pname = '. . . . ' * (ob.path.count(',') - 1)
    context = {'typeslist': list}
    return render(request, 'myadmin/type/index.html', context)


def add(request, tid):
    '''加载添加页面'''
    # 获取父类别的信息
    print(tid)
    print(type(tid))
    if tid == 0:
        context = {'pid': 0, 'path': '0,', 'name': '根类别'}
    else:
        ob = Types.objects.get(id=tid)
        context = {'pid': ob.id, 'path': ob.path + str(ob.id) + ',', 'name': ob.name}
    return render(request, 'myadmin/type/add.html', context)


def insert(request):
    '''执行添加'''
    try:
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        ob.path = request.POST['path']
        ob.save()
        context = {'info': '添加成功'}
    except Exception as e:
        print(e)
        context = {'info': '添加失败'}
    return render(request, 'myadmin/info.html', context)


def delete(request, tid):
    '''删除信息'''
    try:
        if Types.objects.filter(pid=tid):
            context = {'info': '删除失败，此类别下还有子类别'}
        else:
            ob = Types.objects.get(id=tid)
            ob.delete()
            context = {'info': '删除成功'}
    except Exception as e:
        print(e)
        context = {'info': '删除失败'}
    return render(request, 'myadmin/info.html', context)


def edit(request, tid):
    '''加载编辑页面'''
    try:
        # print(uid)
        ob = Types.objects.get(id=tid)
        context = {'types': ob}
        return render(request, 'myadmin/type/edit.html', context)
    except Exception as e:
        print(e)
        context = {'info': '没有找到要修改的信息'}
    return render(request, 'myadmin/info.html', context)


def update(request, tid):
    '''执行信息编辑'''
    try:
        type = Types.objects.get(id=tid)
        type.name = request.POST['name']
        type.save()
        context = {'info': '修改成功'}
    except Exception as e:
        print(e)
        context = {'info': '修改失败'}

    return render(request, 'myadmin/info.html', context)


def editor(request):
    return render(request, 'myadmin/type/editor.html')
