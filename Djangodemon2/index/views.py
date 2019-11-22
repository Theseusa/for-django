from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.core import serializers
from .models import *
from .forms import *
import json

# Create your views here.
def index_views(request):
    return render(request,'index.html')

def login_views(request):
    if request.method == 'GET':
        url = request.META.get('HTTP_REFERER','/')
        if 'uid' in request.session and 'uphone' in request.session:
            resp = HttpResponse(url)
            return resp
        else:
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid']=uid
                request.session['uphone']=uphone
                resp = redirect(url)
                return  resp
            else:
                form = LoginForm()
                resp =  render(request,'login.html',locals())
                resp.set_cookie('url',url)
                return resp

    else:
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        users = User.objects.filter(upwd=upwd,uphone=uphone)
        if users:
            request.session['uid'] = users[0].id
            request.session['uphone'] = uphone
            url = request.COOKIES.get('url','/')
            resp = redirect(url)
            if url in request.COOKIES:
                resp.delete_cookie('url')
            if 'isSaved' in request.POST:
                expire = 60*60*24*90
                resp.set_cookie('uid',users[0].id,expire)
                resp.set_cookie('uphone',uphone,expire)
            return resp
        else:
            # 登录失败
            form = LoginForm()
            return render(request,'login.html',locals())



    return render(request,'login.html',locals())

def register_views(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        uphone = request.POST['uphone']
        users = User.objects.filter(uphone=uphone)
        if users:
            errMsg = '手机号码已经存在'
            return render(request,'register.html',locals())
        upwd = request.POST['upwd']
        uname = request.POST['uname']
        uemail = request.POST['uemail']
        user = User()
        user.uphone = uphone
        user.upwd = upwd
        user.uname = uname
        user.uemail = uemail
        user.save()
        request.session['uid'] = user.id
        request.session['uphone'] = user.uphone
        return HttpResponse("register OK")


def check_uphone_views(request):
    uphone = request.GET['uphone']
    users = User.objects.filter(uphone=uphone)
    if users:
        status = 1
        msg = '手机号码已经存在'
    else:
        status = 0
        msg = '通过'
    dic =   {
        'status':status,
        'msg':msg,
    }
    return HttpResponse(json.dumps(dic))


def check_login_views(request):
  if 'uid' in request.session and 'uphone' in request.session:
    loginStatus = 1
    #通过uid的值获取对应的uname
    id = request.session['uid']
    uname=User.objects.get(id=id).uname
    dic = {
      'loginStatus':loginStatus,
      'uname':uname
    }
    return HttpResponse(json.dumps(dic))
  else:
    dic = {
      'loginStatus':0
    }
    return HttpResponse(json.dumps(dic))

def logout_views(request):
  #判断session中是否有登录信息，有的话则清除
  if 'uid' in request.session and 'uphone' in request.session:
    del request.session['uid']
    del request.session['uphone']
    #构建响应对象：哪发的退出请求，则返回到哪去
    url=request.META.get('HTTP_REFERER','/')
    resp = HttpResponseRedirect(url)
    #判断cookies中是否有登录信息，有的话，则删除
    if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
      resp.delete_cookie('uid')
      resp.delete_cookie('uphone')
    return resp
  return redirect('/')

def type_goods_views(request):
  all_list = []
  #加载所有的商品类型
  types = GoodsType.objects.all()
  for type in types:
    type_json = json.dumps(type.to_dict())
    #获取type类型下的最新的10条数据
    g_list = type.goods_set.filter(isActive=True).order_by("-id")[0:10]
    #将g_list转换为json
    g_list_json=serializers.serialize('json',g_list)
    #将type_json和g_list_json封装到一个字典中
    dic = {
      "type":type_json,
      "goods":g_list_json,
    }
    #将dic字典追加到all_list中
    all_list.append(dic)
  return HttpResponse(json.dumps(all_list))

def add_cart_views(request):
  #获取商品id,获取用户id,购买数量默认为1
  good_id=request.GET['gid']
  user_id = request.session['uid']
  ccount = 1
  #查看购物车中是否有相同用户购买的相同商品
  cart_list = CartInfo.objects.filter(user_id=user_id,goods_id=good_id)
  if cart_list:
    #已经有相同用户购买过相同产品了,更新商品数量
    cartinfo = cart_list[0]
    cartinfo.ccount = cartinfo.ccount + ccount
    cartinfo.save()
    dic = {
      'status':1,
      'statusText':'更新数量成功'
    }
  else:
    #没有对应的用户以及对应的商品
    cartinfo = CartInfo()
    cartinfo.user_id = user_id
    cartinfo.goods_id = good_id
    cartinfo.ccount = ccount
    cartinfo.save()
    dic = {
      'status':1,
      'statusText':'添加购物车成功'
    }
  return HttpResponse(json.dumps(dic))
