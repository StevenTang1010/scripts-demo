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
from django.urls import path, include, re_path
from .views import index, users, types, goods, orders

urlpatterns = [
    # 后台首页
    path('', index.index, name='myadmin_index'),  # 后台首页

    # 后台管理员路由
    path('login', index.login, name='myadmin_login'),
    path('dologin', index.dologin, name='myadmin_dologin'),
    path('logout', index.logout, name='myadmin_logout'),
    path('verify', index.verify, name='myadmin_verify'),

    # 会员信息管理路由
    path('users/<int:pageindex>', users.index, name='myadmin_users_index'),
    path('users/add', users.add, name='myadmin_users_add'),
    path('users/insert', users.insert, name='myadmin_users_insert'),
    path('users/del/<int:uid>', users.delete, name='myadmin_users_del'),
    path('users/edit/<int:uid>', users.edit, name='myadmin_users_edit'),
    path('users/update/<int:uid>', users.update, name='myadmin_users_update'),
    path('users/reset/<int:uid>', users.reset, name='myadmin_users_reset'),
    path('users/doreset/<int:uid>', users.do_reset, name='myadmin_users_doreset'),

    # 商品类别信息管理路由
    path('type', types.index, name='myadmin_type_index'),
    path('type/add/<int:tid>', types.add, name='myadmin_type_add'),
    path('type/insert', types.insert, name='myadmin_type_insert'),
    path('type/del/<int:tid>', types.delete, name='myadmin_type_del'),
    path('type/edit/<int:tid>', types.edit, name='myadmin_type_edit'),
    path('type/update/<int:tid>', types.update, name='myadmin_type_update'),
    path('type/editor', types.editor, name='myadmin_type_editor)'),

    # 商品信息管理路由
    path('goods/<int:pageindex>', goods.index, name='myadmin_goods_index'),
    path('goods/add', goods.add, name='myadmin_goods_add'),
    path('goods/insert', goods.insert, name='myadmin_goods_insert'),
    path('goods/del/<int:gid>', goods.delete, name='myadmin_goods_del'),
    path('goods/edit/<int:gid>', goods.edit, name='myadmin_goods_edit'),
    path('goods/update/<int:gid>', goods.update, name='myadmin_goods_update'),
    # path('users/reset/<int:uid>', goods.reset, name='myadmin_goods_reset'),
    # path('users/doreset/<int:uid>', goods.do_reset, name='myadmin_goods_doreset'),

    # 订单管理
    path('orders', orders.index, name='myadmin_orders_index'),  #
    path('orders/<int:pIndex>', orders.index, name='myadmin_orders_index'),  #
    path('orders/detail/<int:oid>', orders.detail, name='myadmin_orders_detail'),  #
    path('orders/state', orders.state, name='myadmin_orders_state'),  #
]
