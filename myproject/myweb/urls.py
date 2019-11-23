"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from .views import index, cart, orders, vip


urlpatterns = [
    path('', index.index, name='index'),  # 前台首页
    path('list', index.lists, name='lists'),  # 商品列表
    path('list/<int:pageindex>', index.lists, name='lists'),  # 分页展示
    path('detail/<int:gid>', index.detail, name='detail'),  # 商品详情

    # 会员及个人中心等路由配置
    path('login', index.login, name='login'),
    path('dologin', index.dologin, name='dologin'),
    path('logout', index.logout, name='logout'),
    path('register', index.register, name='register'),
    path('doregister', index.doregister, name='doregister'),
    path('verify', index.verify, name='verify'),

# 购物车信息管理路由配置
    path('cart', cart.index, name='cart_index'),
    path('cart/add/<int:gid>', cart.add, name='cart_add'),
    path('cart/delete/<int:gid>', cart.delete, name='cart_delete'),
    path('cart/clear', cart.clear, name='cart_clear'),
    path('cart/change', cart.change, name='cart_change'),

# 订单处理
    path('orders/add', orders.add, name='orders_add'),  # 订单的表单页面
    path('orders/confirm', orders.confirm, name='orders_confirm'),  # 订单确认页
    path('orders/insert', orders.insert, name='orders_insert'),  # 执行订单添加

# 会员中心
    path('vip/orders', vip.viporders, name='vip_orders'),  # 会员中心我的订单
    path('vip/orders/<int:state>', vip.viporders, name='vip_orders'),  # 会员中心我的订单
    path('vip/odstate', vip.odstate, name='vip_odstate'),  # 修改订单状态（确认收货）
    path('vip/info', vip.info, name='vip_info'),  # 会员中心的个人信息
    path('vip/update', vip.update, name='vip_update'),  # 执行修改会员信息
    path('vip/resetps', vip.resetps, name='vip_resetps'),  # 重置密码表单
    path('vip/doresetps', vip.doresetps, name='vip_doresetps'),  # 执行重置密码

]
