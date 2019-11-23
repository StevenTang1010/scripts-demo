from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from common.models import Users, Types, Goods
from ..forms import ResetPwdForm
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
# 公共信息加载函数
def loadinfo(request):
    list = Types.objects.filter(pid=0)
    context = {'typelist': list}
    return context

# 网站商品展示
def index(request):
    '''项目前台首页'''
    context = loadinfo(request)
    goods = Goods.objects.order_by('-clicknum')[:5]
    # clothing = goods.filter(typeid__in=Types.objects.only('id').filter(pid=1)).order_by('-addtime')[:4]
    # phonelist = goods.filter(typeid__in=Types.objects.only('id').filter(pid=2)).order_by('-addtime')[:4]
    # context['goodslist'] = goods

    return render(request, 'myweb/index.html', context)


def lists(request, pageindex=1):
    '''商品列表页'''
    context = loadinfo(request)
    # 查询商品信息
    goods = Goods.objects
    tid = int(request.GET.get('tid', 0))
    parmlist = []
    if tid > 0:
        list = goods.filter(typeid__in=Types.objects.only('id').filter(pid=tid))
        parmlist.append('tid=' + str(tid))
        goods = request.GET.get('goods')
        if goods:
            list = list.filter(Q(goods__contains=goods))
            parmlist.append('goods=' + goods)
        else:
            list = list.all().order_by('id')
        pages = Paginator(list, 8)  # 分页
        maxpages = pages.num_pages
        goodslist = pages.page(pageindex)  # 保存分页后的当前页信息
        plist = pages.page_range  # 保存页码列表
        if pageindex > maxpages:
            pageindex = maxpages
        if pageindex < maxpages:
            pageindex = 1
        context['goodslist'] = goodslist
        context['plist'] = plist
        context['pageindex'] = pageindex
        context['parmlist'] = parmlist
        context['maxpages'] = maxpages
    else:
        list = goods.filter()
        goods = request.GET.get('goods')
        if goods:
            list = list.filter(Q(goods__contains=goods))
            parmlist.append('goods=' + goods)
        else:
            list = list.all().order_by('id')
        pages = Paginator(list, 8)  # 分页
        maxpages = pages.num_pages
        goodslist = pages.page(pageindex)  # 保存分页后的当前页信息
        pagelist = pages.page_range  # 保存页码列表
        if pageindex > maxpages:
            pageindex = maxpages
        if pageindex < maxpages:
            pageindex = 1
        context['goodslist'] = goodslist
        context['pagelist'] = pagelist
        context['pageindex'] = pageindex
        context['parmlist'] = parmlist
        context['maxpages'] = maxpages
    return render(request, 'myweb/list.html', context)


def detail(request, gid):
    '''商品详情页'''
    context = loadinfo(request)
    ob = Goods.objects.get(id=gid)
    ob.clicknum += 1
    ob.save()
    context['goods'] = ob
    return render(request, 'myweb/detail.html', context)


# 登录相关操作
def login(request):
    '''会员登陆表单'''
    return render(request, 'myweb/login.html')


def dologin(request):
    '''会员执行登陆'''
    # 校验验证码
    verifycode = request.session['verifycode']
    code = request.POST['code']
    if verifycode != code:
        context = {'info': '验证码错误'}
        return render(request, 'myweb/login.html', context)

    try:
        # 根据账号获取登陆者信息
        user = Users.objects.get(username=request.POST['username'])
        # 判断当前用户是否是后台管理员用户
        if user.state == 0 or user.state == 1:
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'], encoding='utf-8'))
            if user.password == m.hexdigest():
                # 此处登陆成功,将当前登陆信息放入到session中，并跳转
                request.session['vipuser'] = user.toDict()
                return redirect(reverse('index'))
            else:
                context = {'info': '登陆密码错误!'}
        else:
            context = {'info': '非法用户！'}
    except:
        context = {'info': '登陆账号错误'}
    return render(request, 'myweb/login.html', context)


def logout(request):
    '''会员登出'''
    # 清除登录的session信息
    del request.session['vipuser']
    # 跳转回登录页面（url地址改变）
    return redirect(reverse('login'))


def register(request):
    '''会员注册'''
    return render(request, 'myweb/register.html')

def doregister(request):
    '''会员注册'''
    ob = Users()
    form = ResetPwdForm(request.POST)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        # md5只能接收bytes数据类型
        # 在Python3中，默认的字符串都是str类型
        # 所以这里要把str变成bytes类型
        import hashlib
        ob.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        ob.username = request.POST['username']
        return render(request, 'myweb/login.html')
    else:
        context = {
            'info': '两次密码不一致'
        }
        return render(request, 'myweb/info.html', context)


def verify(request):
    '''验证码'''
    import random
    from PIL import Image, ImageDraw, ImageFont
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (242, 164, 247)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的poing()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随即选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    print(rand_str)
    # 构造字体对象，
    font = ImageFont.truetype('static/msyh.ttc', 21)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, -2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # python3内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
