import re
from django.shortcuts import redirect
from django.urls import reverse


class shopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        # print('shopMiddleware')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # print('mycall.....'+request.path)
        urllist = ['/myadmin/login', '/myadmin/dologin', '/myadmin/logout', '/myadmin/verify']
        # 获取当前请求路径
        path = request.path
        # 判断当前请求是否是访问网站后台，并且path不在urllist中
        if re.match('/myadmin', path) and (path not in urllist):
            # 判断当前用户是否没有登陆
            if 'adminuser' not in request.session:
                return redirect(reverse('myadmin_login'))

        # 网站前台会员登陆判断
        if re.match('^/orders', path) or re.match('^/vip', path):
            # 判断当前会员是否没有登陆
            if 'vipuser' not in request.session:
                return redirect(reverse('login'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
