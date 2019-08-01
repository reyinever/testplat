from django.shortcuts import render,redirect

# Create your views here.

from django.http import HttpResponse,JsonResponse
from apitest.models import UserInfo
from datetime import datetime
from module.models import ModuleInfo
from product.models import ProductInfo
from apitest.models import ApicaseInfo
from django.views.decorators import csrf
from django.core.paginator import Paginator
from commont.public_var import per_page_rows
from apitest.models import ApiInfo
from apitest.models import ApisInfo


# /apitest/register/
def register(request):
    """注册页面"""
    return render(request,'apitest/register.html')


# /apitest/register_check/
def register_check(request):
    """注册验证"""
    if request.method=='POST':
        username = request.POST.get('username','')
        password1=request.POST.get('password1','')
        password2=request.POST.get('password2','')
        email=request.POST.get('email','')
        print(username,password1,password2,email)
        if not username or not password1 or not password2 or not email:
            msg='有必填项未填写'
            return render(request,'apitest/register.html',{'message':msg})
            # data={'code':0,'mssage':msg}
            # return JsonResponse({'data':data})
        if password1 != password2:
            msg='密码和确认密码不一样'
            return render(request,'apitest/register.html',{'message':msg})
            # data={'code':0,'message':msg}
            # return JsonResponse({'data':data})
        usernames=UserInfo.objects.filter(username=username)
        # print(len(usernames))
        # print('usernames:',usernames)
        if len(usernames):
            msg='用户名已存在'
            # return render(request,'apitest/register.html',{'message':msg})
            return render(request,'apitest/register.html',{'message':msg})
            # data = {'code': 0, 'message': msg}
            # return JsonResponse({'data':data})
        # UserInfo.objects.create(username=username,password=password1,email=email,createtime=datetime.now())
        msg = '恭喜你，注册成功！'
        # return render(request,'apitest/login.html',{'succ_message':msg})
        return redirect('/apitest/login/')
        # data = {'code': 0, 'message': msg}
        # return JsonResponse({'data':data})
    else:
        return redirect('/apitest/register/')


# /apitest/login/
def login(request):
    """登录页面"""
    if 'is_login' in request.session:
        # 如果用户已经登录
        return redirect('/apitest/index/')
    else:
        # 用户未登录
        if 'username' in request.COOKIES:
            username=request.COOKIES.get('username')
        else:
            username=''
        succ_message=""
        err_message=""
        return render(request,'apitest/login.html',{'username':username,'succ_message':succ_message,'err_message':err_message})


# 生成验证码
from PIL import Image,ImageDraw,ImageFont
from django.utils.six import BytesIO

# /apitest/login_verify_code/
def login_verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高  RGB
    bgcolor=(random.randrange(20,100),random.randrange(20,100),255)
    width=100
    height=25
    # 创建画布对象
    im=Image.new('RGB',(width,height),bgcolor)
    # 创建画笔对象
    draw=ImageDraw.Draw(im)
    # 调用画笔的 point() 函数绘制噪点
    for i in range(0,100):
        xy=(random.randrange(0,width),random.randrange(0,height))
        fill=(random.randrange(0,255),255,random.randrange(0,255))
        draw.point(xy,fill=fill)
    # 定义验证码的备选值
    import string
    # 随机取 4 个值作为验证码
    rand_str="".join(random.sample(string.ascii_letters+string.digits,4))
    # 构造字体对象 windows的字体路径在 C:\Windows\Fonts
    font=ImageFont.truetype('C:\Windows\Fonts\simsun.ttc',25,index=1)
    # 构造字体颜色
    fontcolor=(255,random.randrange(0,255),random.randrange(0,255))
    # 绘制4个字
    draw.text((5,1),rand_str[0],font=font,fill=fontcolor)
    draw.text((25,1),rand_str[1],font=font,fill=fontcolor)
    draw.text((50, 1), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 1), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 把验证码存入session,用于做进一步的验证
    request.session['verifycode']=rand_str
    # 内存文件操作
    buf=BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf,'png')
    # 将内存中的图片数据返回给客户端 .MIME 类型为图片png
    return HttpResponse(buf.getvalue(),'image/png')


# /apitest/login_check/
def login_check(request):
    """登录验证"""
    if request.method=='POST':
        username=request.POST.get('username')  # 用户名
        password=request.POST.get('password')   # 密码
        inputverifycode=request.POST.get('vcode')  # 输入的验证码
        remberme=request.POST.get('remberme')    # 记住密码
        verifycode=request.session.get('verifycode')  # 产生的验证码

        print(username,password,inputverifycode,remberme,verifycode)

        if inputverifycode!=verifycode:
            # 验证码错误
            msg='验证码错误'
            if not inputverifycode:
                # 不输入验证码，刷新页面，不显示错误提示
                msg=''
            return render(request,'apitest/login.html',{'err_message':msg,'succ_message':''})
        user_info=UserInfo.objects.filter(username=username,password=password )
        if(len(user_info)):
            # 用户信息正确
            response=redirect('/apitest/index')
            if remberme=='on':
                # 记住密码
                response.set_cookie('username',username,max_age=365*24*3600)
                # response.set_cookie('password',password,max_age=365*24*3600)
            # 标记登录状态
            request.session['is_login']=True
            # 保存用户名
            request.session['user']=username
            return response
        else:
            msg='用户名密码错误'
            return render(request,'apitest/login.html',{'err_message':msg,'succ_message':''})
    return redirect('/apitest/login/')

"""
自定义登录装饰器
"""
def login_reqiured(view_func):
    """登录判断装饰器"""
    def wrapper(request,*view_args,**view_kwargs):
        if 'is_login' in request.session:
            # 用户已登录
            return view_func(request,*view_args,**view_kwargs)
        else:
            # 用户未登录
            return redirect('/apitest/login/')
    return wrapper


# #############    接口管理部分    #############


# /apitest/login/
@login_reqiured
def index(request):
    """接口列表页"""
    username = request.session.get('user')
    apis = ApiInfo.objects.all()
    api_count = ApiInfo.objects.all().count()
    page = request.GET.get('page', '')
    paginator = Paginator(apis, per_page_rows)
    try:
        if page == '':
            page = 1
        else:
            page = int(page)
            if page > paginator.num_pages:
                page = paginator.num_pages
        api_list = paginator.page(page)
        return render(request, 'apitest/apitest_index.html', {'username': username,
                                                              'apis': api_list,
                                                              'api_count': api_count
                                                              })
    except Exception as e:
        print('接口列表异常：', e)
        render(request, 'apitest/apitest_index.html', {'username': username, 'err_msg': '用例列表异常，请稍后再试！'})


# /apitest/add
def apitest_add(request):
    """接口新增页面"""
    return render(request,'apitest/apitest_add.html')


# /apitest/add_check/
@csrf.csrf_exempt
def apitest_add_check(request):
    """添加接口验证"""
    if request.method=="POST":
        # 获取请求数据
        product_id=request.POST.get('product_id')
        module_id=request.POST.get('module_id')
        interface_name=request.POST.get('interface_name')
        interface_url=request.POST.get('interface_url')
        interface_method=request.POST.get('interface_method')
        # print('method:',interface_method)
        interface_param=request.POST.get('interface_param')
        interface_others=request.POST.get('interface_others')

        if not product_id or product_id=='default':
            data={'code':'0','message':'请选择产品名称！'}
            return JsonResponse({'data':data})
        if not module_id or module_id=='default':
            data={'code':'0','message':'请选择模块名称！'}
            return JsonResponse({'data':data})
        if not interface_name:
            data={'code':'0','message':'接口名称不能为空'}
            return JsonResponse({'data':data})
        if not interface_url:
            data={'code':'0','message':'接口地址不能为空'}
            return JsonResponse({'data':data})
        if not interface_method:
            data={'code':'0','message':'请求方法不能为空'}
            return JsonResponse({'data':data})
        interface_name_exists=ApiInfo.objects.filter(interface_name=interface_name)
        print(interface_name_exists)
        print('用例名称存在数量:',len(interface_name_exists))
        if len(interface_name_exists):
            data={'code':'0','message':'接口名称已存在'}
            return JsonResponse({'data':data})
        try:
            product=ProductInfo.objects.get(id=int(product_id))
            module=ModuleInfo.objects.get(id=int(module_id))
            ApiInfo.objects.create(product_id=product,
                                   module_id=module,
                                   interface_name= interface_name,
                                   interface_url= interface_url,
                                   interface_method= interface_method,
                                   interface_param= interface_param,
                                   interface_others= interface_others,
                                   create_time=datetime.now())
            data={'code':'1','message':'操作成功'}
            return JsonResponse({'data':data})
        except Exception as e:
            print('新接口异常：',e)
            data={'code':'0','message':'未知错误：%s'%e}
            return JsonResponse({'data':data})
    else:
        data={'code':'0','message':'请求方法不正确'}
        return JsonResponse({'data':data})


# /apitest/detail/<int:id>
def apitest_detail(request,apiid):
    """接口详情页面"""
    username = request.session.get('user')
    try:
        api = ApiInfo.objects.get(id=apiid)
        return render(request, 'apitest/apitest_detail.html', {'username': username,
                                                               'api': api
                                                               })
    except Exception as e:
        print('用例详情页异常：', e)
        return render(request, 'apitest/apitest_detail.html', {'username': username,
                                                               'err_msg': e})


# /apitest/change/<int:id>
def apitest_change(request,apiid):
    """接口信息修改页面"""
    username = request.session.get('user')
    try:
        api = ApiInfo.objects.get(id=apiid)
        return render(request, 'apitest/apitest_change.html', {'username': username,
                                                               'api': api
                                                               })
    except Exception as e:
        print('接口修改页异常：', e)
        return render(request, 'apitest/apitest_change.html', {'username': username,
                                                               'err_msg': e})



# /apitest/change_check/
@csrf.csrf_exempt
def apitest_change_check(request):
    """用例修改"""
    if request.method=="POST":
        # 获取请求数据
        product_id=request.POST.get('product_id')
        module_id=request.POST.get('module_id')
        print('mid:',module_id)
        apiid=request.POST.get('api_id')
        api_name=request.POST.get('api_name')
        api_url=request.POST.get('api_url')
        api_method=request.POST.get('api_method')
        # print('method:',api_method)
        api_param=request.POST.get('api_param')
        api_others=request.POST.get('api_others')
        if not product_id or product_id=='default':
            data={'code':'0','message':'请选择产品名称！'}
            return JsonResponse({'data':data})
        if not module_id or module_id=='default':
            data={'code':'0','message':'请选择模块名称！'}
            return JsonResponse({'data':data})
        if not api_name:
            data={'code':'0','message':'接口名称不能为空'}
            return JsonResponse({'data':data})
        if not api_url:
            data={'code':'0','message':'请求地址不能为空'}
            return JsonResponse({'data':data})
        if not api_method:
            data={'code':'0','message':'请求方式不能为空'}
            return JsonResponse({'data':data})
        api_name_exists=ApiInfo.objects.filter(interface_name=api_name).exclude(id=int(apiid))
        print(api_name_exists)
        print('用例名称存在数量:',len(api_name_exists))
        if len(api_name_exists):
            data={'code':'0','message':'接口名称已存在'}
            return JsonResponse({'data':data})
        try:
            api=ApiInfo.objects.get(id=int(apiid))
            # product = ProductInfo.objects.get(id=int(product_id))
            # apicase.product_id=product
            api.product_id_id=int(product_id)
            # module = ModuleInfo.objects.get(id=int(module_id),product_id=product)
            # print('mobj:',module)
            api.module_id_id=int(module_id)
            api.interface_name=api_name
            api.interface_url= api_url
            api.interface_method= api_method
            api.interface_param= api_param
            api.interface_others= api_others
            api.create_time=datetime.now()
            api.save()
            data={'code':'1','message':'操作成功'}
            return JsonResponse({'data':data})
        except Exception as e:
            print('修改接口异常：',e)
            data={'code':'0','message':'未知错误：%s'%e}
            return JsonResponse({'data':data})
    else:
        data={'code':'0','message':'请求方式不正确'}
        return JsonResponse({'data':data})


# /apitest/delete/
@csrf.csrf_exempt
def apitest_delete(request):
    """删除接口信息"""
    if request.method=='POST':
        apiid = request.POST.get('id')
        apiname = request.POST.get('name')
        api_exists = ApiInfo.objects.filter(id=apiid, interface_name=apiname)
        if len(api_exists):
            api_exists.delete()
            data = {'code': '1', 'message': '删除成功！'}
        else:
            data = {'code': '0', 'message': '删除的数据不存在！'}
        return JsonResponse({'data': data})
    else:
        data = {'code': '0', 'message': '请求方式不正确！'}
        return JsonResponse({'data': data})


# /apitest/search/?interface_name=xxx
def apitest_search(request):
    """接口查找页面"""
    username = request.session.get('user')
    api_name = request.GET.get('interface_name')
    apis = ApiInfo.objects.filter(interface_name=api_name)
    if len(apis):
        return render(request, 'apitest/apitest_index.html', {'username': username, 'apis': apis})
    else:
        return render(request, 'apitest/apitest_index.html', {'username': username, 'err_msg': '无数据'})


# ############# 退出登录  #############
# /apitest/logout/
def logout(request):
    """退出登录"""
    request.session.clear()
    return redirect('/apitest/login/')


# #############     接口用例 部分   #############   #


# /apitest/apicase/
def apicase(request):
    """接口用例页面"""
    username = request.session.get('user')
    apicases=ApicaseInfo.objects.all()
    apicase_count=ApicaseInfo.objects.all().count()
    page=request.GET.get('page','')
    paginator = Paginator(apicases, per_page_rows)
    try:
        if page=='':
            page=1
        else:
            page=int(page)
            if page>paginator.num_pages:
                page=paginator.num_pages
        apicase_list=paginator.page(page)
        return render(request,'apitest/apicase.html',{'username':username,
                                                      'apicases':apicase_list,
                                                      'apicase_count':apicase_count
                                                      })
    except Exception as e:
        print('用例列表异常：',e)
        render(request,'apitest/apicase.html',{'username':username,'err_msg':'用例列表异常，请稍后再试！'})


# /apitest/apicase/add/
def apicase_add(request):
    """新增接口用例"""
    username=request.session.get('user')
    return render(request,'apitest/apicase_add.html',{'username':username})


# /apitest/get_module_names/
def get_module_names(request):
    """获取模块名称"""
    modules=ModuleInfo.objects.all()
    if len(modules):
        data=[]
        for m in modules:
            data.append((m.id,m.module_name))
        return JsonResponse({'data':data})
    else:
        return JsonResponse({'data':0})


# /apitest/pid<int:pid>/module_names/
def pid_module_names(request,pid):
    """获取产品下的模块名称"""
    pid=int(pid)
    # print('pid:',pid)
    modules=ModuleInfo.objects.filter(product_id__id=pid)
    # print(modules)
    if len(modules):
        data=[]
        for m in modules:
            data.append((m.id,m.module_name))
        return JsonResponse({'data':data})
    else:
        return JsonResponse({'data':'0'})


# /apitest/apcase/add_check/
@csrf.csrf_exempt
def apicase_add_check(request):
    """新增用例验证"""
    if request.method=="POST":
        # 获取请求数据
        product_id=request.POST.get('product_id')
        module_id=request.POST.get('module_id')
        apicase_name=request.POST.get('apicase_name')
        apicase_desc=request.POST.get('apicase_desc')
        # print('apicase_desc:',apicase_desc)
        apicase_url=request.POST.get('apicase_url')
        apicase_method=request.POST.get('apicase_method')
        # print('method:',apicase_method)
        apicase_head=request.POST.get('apicase_head')
        apicase_param=request.POST.get('apicase_param')
        apicase_relydata=request.POST.get('apicase_relydata')
        print('relydata:',apicase_relydata)
        apicase_execute=request.POST.get('apicase_execute')
        apicase_assert=request.POST.get('apicase_assert')
        apicase_needstore=request.POST.get('apicase_needstore')
        apicase_others=request.POST.get('apicase_others')

        if not product_id or product_id=='default':
            data={'code':'0','message':'请选择产品名称！'}
            return JsonResponse({'data':data})
        if not module_id or module_id=='default':
            data={'code':'0','message':'请选择模块名称！'}
            return JsonResponse({'data':data})
        if not apicase_name:
            data={'code':'0','message':'用例名称不能为空'}
            return JsonResponse({'data':data})
        if not apicase_url:
            data={'code':'0','message':'请求地址不能为空'}
            return JsonResponse({'data':data})
        if not apicase_method:
            data={'code':'0','message':'请求方式不能为空'}
            return JsonResponse({'data':data})
        apicase_name_exists=ApicaseInfo.objects.filter(apicase_name=apicase_name)
        print(apicase_name_exists)
        print('用例名称存在数量:',len(apicase_name_exists))
        if len(apicase_name_exists):
            data={'code':'0','message':'用例名称已存在'}
            return JsonResponse({'data':data})
        try:
            product=ProductInfo.objects.get(id=int(product_id))
            module=ModuleInfo.objects.get(id=int(module_id))
            ApicaseInfo.objects.create(product_id=product,
                                       module_id=module,
                                       apicase_name= apicase_name,
                                       apicase_desc=apicase_desc,
                                       apicase_url= apicase_url,
                                       apicase_method= apicase_method,
                                       apicase_head= apicase_head,
                                       apicase_param= apicase_param,
                                       apicase_relydata= apicase_relydata,
                                       apicase_execute= apicase_execute,
                                       apicase_assert= apicase_assert,
                                       apicase_needstore= apicase_needstore,
                                       apicase_others= apicase_others,
                                       create_time=datetime.now())
            data={'code':'1','message':'操作成功'}
            return JsonResponse({'data':data})
        except Exception as e:
            print('新增用例异常：',e)
            data={'code':'0','message':'未知错误：%s'%e}
            return JsonResponse({'data':data})
    else:
        data={'code':'0','message':'请求方式不正确'}
        return JsonResponse({'data':data})


# /apitest/apicase/search/
def apicase_search(request):
    """用例名称查找"""
    username=request.session.get('user')
    apicase_name=request.GET.get('apicase_name')
    apicases=ApicaseInfo.objects.filter(apicase_name=apicase_name)
    if len(apicases):
        return render(request,'apitest/apicase.html',{'username':username,'apicases':apicases})
    else:
        return render(request,'apitest/apicase.html',{'username':username,'err_msg':'无数据'})


# /apitest/apicase/detail/{{ apicase.id }
def apicase_detail(request,acid):
    """用例详情页"""
    username = request.session.get('user')
    try:
        apicase = ApicaseInfo.objects.get(id=acid)
        return render(request, 'apitest/apicase_detail.html', {'username': username,
                                                               'apicase': apicase
                                                               })
    except Exception as e:
        print('用例详情页异常：', e)
        return render(request, 'apitest/apicase_detail.html', {'username': username,
                                                               'err_msg': e})


# /apitest/apicase/change/{{ apicase.id }
def apicase_change(request,acid):
    """用例修改页"""
    username=request.session.get('user')
    try:
        apicase=ApicaseInfo.objects.get(id=acid)
        return render(request,'apitest/apicase_change.html',{'username':username,
                                                         'apicase':apicase
                                                         })
    except Exception as e:
        print('用例修改页异常：',e)
        return render(request,'apitest/apicase_change.html',{'username':username,
                                                             'err_msg':e})


# /apitest/apicase/change_check/
@csrf.csrf_exempt
def apicase_change_check(request):
    """用例修改"""
    if request.method=="POST":
        # 获取请求数据
        product_id=request.POST.get('product_id')
        module_id=request.POST.get('module_id')
        print('mid:',module_id)
        acid=request.POST.get('apicase_id')
        apicase_name=request.POST.get('apicase_name')
        apicase_desc=request.POST.get('apicase_desc')
        apicase_url=request.POST.get('apicase_url')
        apicase_method=request.POST.get('apicase_method')
        # print('method:',apicase_method)
        apicase_head=request.POST.get('apicase_head')
        apicase_param=request.POST.get('apicase_param')
        apicase_relydata=request.POST.get('apicase_relydata')
        apicase_execute=request.POST.get('apicase_execute')
        apicase_assert=request.POST.get('apicase_assert')
        apicase_needstore=request.POST.get('apicase_needstore')
        apicase_others=request.POST.get('apicase_others')

        if not product_id or product_id=='default':
            data={'code':'0','message':'请选择产品名称！'}
            return JsonResponse({'data':data})
        if not module_id or module_id=='default':
            data={'code':'0','message':'请选择模块名称！'}
            return JsonResponse({'data':data})
        if not apicase_name:
            data={'code':'0','message':'用例名称不能为空'}
            return JsonResponse({'data':data})
        if not apicase_url:
            data={'code':'0','message':'请求地址不能为空'}
            return JsonResponse({'data':data})
        if not apicase_method:
            data={'code':'0','message':'请求方式不能为空'}
            return JsonResponse({'data':data})
        apicase_name_exists=ApicaseInfo.objects.filter(apicase_name=apicase_name).exclude(id=int(acid))
        print(apicase_name_exists)
        print('用例名称存在数量:',len(apicase_name_exists))
        if len(apicase_name_exists):
            data={'code':'0','message':'用例名称已存在'}
            return JsonResponse({'data':data})
        try:
            apicase=ApicaseInfo.objects.get(id=int(acid))
            # product = ProductInfo.objects.get(id=int(product_id))
            # apicase.product_id=product
            apicase.product_id_id=int(product_id)
            # module = ModuleInfo.objects.get(id=int(module_id),product_id=product)
            # print('mobj:',module)
            apicase.module_id_id=int(module_id)
            apicase.apicase_name=apicase_name
            apicase.apicase_desc=apicase_desc
            apicase.apicase_url= apicase_url
            apicase.apicase_method= apicase_method
            apicase.apicase_head= apicase_head
            apicase.apicase_param= apicase_param
            apicase.apicase_relydata= apicase_relydata
            apicase.apicase_execute= apicase_execute
            apicase.apicase_assert= apicase_assert
            apicase.apicase_needstore= apicase_needstore
            apicase.apicase_others= apicase_others
            apicase.create_time=datetime.now()
            apicase.save()
            data={'code':'1','message':'操作成功'}
            return JsonResponse({'data':data})
        except Exception as e:
            print('修改用例异常：',e)
            data={'code':'0','message':'未知错误：%s'%e}
            return JsonResponse({'data':data})
    else:
        data={'code':'0','message':'请求方式不正确'}
        return JsonResponse({'data':data})


# /apitest/apicase/delete/
@csrf.csrf_exempt
def apicase_delete(request):
    if request.method=='POST':
        acid = request.POST.get('id')
        acname = request.POST.get('name')
        apicase_exists = ApicaseInfo.objects.filter(id=acid, apicase_name=acname)
        if len(apicase_exists):
            apicase_exists.delete()
            data = {'code': '1', 'message': '删除成功！'}
        else:
            data = {'code': '0', 'message': '删除的数据不存在！'}
        return JsonResponse({'data': data})
    else:
        data = {'code': '0', 'message': '请求方式不正确！'}
        return JsonResponse({'data': data})


# ################   流程接口部分      #####################


def apis_index(request):
    """流程接口列表"""
    username = request.session.get('user')
    apiss = ApisInfo.objects.all()
    apis_count = ApisInfo.objects.all().count()
    page = request.GET.get('page', '')
    paginator = Paginator(apiss, per_page_rows)
    try:
        if page == '':
            page = 1
        else:
            page = int(page)
            if page > paginator.num_pages:
                page = paginator.num_pages
        apis_list = paginator.page(page)
        return render(request, 'apitest/apis_index.html', {'username': username,
                                                        'apiss': apis_list,
                                                        'apis_count': apis_count
                                                        })
    except Exception as e:
        print('流程接口列表异常：', e)
        render(request, 'apitest/apis_index.html', {'username': username, 'err_msg': '用例列表异常，请稍后再试！'})


# /apitest/apis/search/
def apis_search(request):
    """流程名称查找"""
    username = request.session.get('user')
    name = request.GET.get('apis_name')
    apiss = ApisInfo.objects.filter(name=name)
    if len(apiss):
        return render(request, 'apitest/apis_index.html', {'username': username, 'apiss': apiss})
    else:
        return render(request, 'apitest/apis_index.html', {'username': username, 'err_msg': '无数据'})


# /apitest/apis/add/
def apis_add(request):
    """新增流程页面"""
    return render(request,'apitest/apis_add.html')


# /apitest/apis/add_check/
@csrf.csrf_exempt
def apis_add_check(request):
    """新增流程验证"""
    if request.method=="POST":
        # 获取请求数据
        # product_id=request.POST.get('product_id')
        # module_id=request.POST.get('module_id')
        executecase=request.POST.get('executecase')
        name=request.POST.get('apis_name')
        desc=request.POST.get('apis_desc')
        execute=request.POST.get('apis_execute')
        others=request.POST.get('apis_others')

        # if not product_id or product_id=='default':
        #     data={'code':'0','message':'请选择产品名称！'}
        #     return JsonResponse({'data':data})
        # if not module_id or module_id=='default':
        #     data={'code':'0','message':'请选择模块名称！'}
        #     return JsonResponse({'data':data})
        if not executecase:
            data={'code':'0','message':'已选用例不能为空'}
            return JsonResponse({'data':data})
        if not name:
            data={'code':'0','message':'流程名称不能为空'}
            return JsonResponse({'data':data})
        name_exists=ApisInfo.objects.filter(name=name)
        print(name_exists)
        print('用例名称存在数量:',len(name_exists))
        if len(name_exists):
            data={'code':'0','message':'流程名称已存在'}
            return JsonResponse({'data':data})
        try:
            # product=ProductInfo.objects.get(id=int(product_id))
            # module=ModuleInfo.objects.get(id=int(module_id))
            ApisInfo.objects.create( # product_id=product,
                                     #  module_id=module,
                                       name=name,
                                       desc=desc,
                                       executecase=executecase,
                                       execute=execute,
                                       others= others,
                                       create_time=datetime.now())
            data={'code':'1','message':'操作成功'}
            return JsonResponse({'data':data})
        except Exception as e:
            print('新增流程异常：',e)
            data={'code':'0','message':'未知错误：%s'%e}
            return JsonResponse({'data':data})
    else:
        data={'code':'0','message':'请求方式不正确'}
        return JsonResponse({'data':data})



def pid_mid_case_names(request,pid,mid):
    """获取指定产品、模块下的用例名称"""
    pid = int(pid)
    mid=int(mid)
    # print('pid:',pid)
    if pid=='' or pid=='default' or mid=='default' or mid=='':
        # data={'code':'0','message':'请选择产品名称或模块名称'}
        return JsonResponse({'data':'请选择产品名称或模块名称'})
    cases = ApicaseInfo.objects.filter(product_id__id=pid,module_id__id=mid)
    print(cases)
    if len(cases):
        data = []
        for c in cases:
            data.append((c.id, c.apicase_name))
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'data': '0'})


def apis_detail(request,apisid):
    """流程详情页"""
    username = request.session.get('user')
    try:
        apis = ApisInfo.objects.get(id=apisid)
        return render(request, 'apitest/apis_detail.html', {'username': username,
                                                               'apis': apis
                                                               })
    except Exception as e:
        print('流程详情页异常：', e)
        return render(request, 'apitest/apis_detail.html', {'username': username,
                                                               'err_msg': e})

def apis_change(request,apisid):
    """流程修改页面"""
    username = request.session.get('user')
    try:
        apis = ApisInfo.objects.get(id=apisid)
        return render(request, 'apitest/apis_change.html', {'username': username,
                                                               'apis': apis
                                                               })
    except Exception as e:
        print('修改流程页面异常：', e)
        return render(request, 'apitest/apis_change.html', {'username': username,
                                                               'err_msg': e})

# /apitest/apis/change_check/
@csrf.csrf_exempt
def apis_change_check(request):
    """修改流程验证"""
    if request.method=="POST":
        # 获取请求数据
        id=request.POST.get('apis_id')
        name=request.POST.get('apis_name')
        desc=request.POST.get('apis_desc')
        executecase=request.POST.get('executecase')
        execute=request.POST.get('apis_execute')
        # print(execute)
        others=request.POST.get('apis_others')
        if not name:
            data={'code':'0','message':'流程名称不能为空'}
            return JsonResponse({'data':data})
        if not executecase:
            data={'code':'0','message':'已选用例不能为空'}
            return JsonResponse({'data':data})
        name_exists=ApisInfo.objects.filter(name=name).exclude(id=int(id))
        print(name_exists)
        print('用例名称存在数量:',len(name_exists))
        if len(name_exists):
            data={'code':'0','message':'流程名称已存在'}
            return JsonResponse({'data':data})
        try:
            apis=ApisInfo.objects.get(id=int(id))
            apis.name=name
            apis.desc= desc
            apis.executecase=executecase
            apis.execute=execute
            apis.others= others
            apis.create_time=datetime.now()
            apis.save()
            data={'code':'1','message':'操作成功'}
            return JsonResponse({'data':data})
        except Exception as e:
            print('修改接口异常：',e)
            data={'code':'0','message':'未知错误：%s'%e}
            return JsonResponse({'data':data})
    else:
        data={'code':'0','message':'请求方式不正确'}
        return JsonResponse({'data':data})


# /apitest/apis/delete/
@csrf.csrf_exempt
def apis_delete(request):
    """删除流程"""
    if request.method=='POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        apis_exists = ApisInfo.objects.filter(id=int(id),name=name)
        if len(apis_exists):
            apis_exists.delete()
            data = {'code': '1', 'message': '删除成功！'}
        else:
            data = {'code': '0', 'message': '删除的数据不存在！'}
        return JsonResponse({'data': data})
    else:
        data = {'code': '0', 'message': '请求方式不正确！'}
        return JsonResponse({'data': data})




#  ########   执行接口测试用例 部分 #############


from commont.api_request import *
import re
from apitest.apicase_utils import request_data_handler
from apitest.apicase_utils import get_assert_result
from apitest.apicase_utils import get_store_data
from apitest.apicase_utils import write_result
from apitest.apicase_utils import write_bug
from apitest.apicase_utils import write_report
from commont.Log import *
import time
from commont.public_var import html_report_path
from commont.html_report import report_html
import os


# /apitest/apicase/run/
def run_apicases(request):
    """运行api用例"""
    # 获取要执行的用例
    execute_case_objs = ApicaseInfo.objects.filter(apicase_execute=True)
    # print(execute_case_objs)
    # 用例总数
    total=execute_case_objs.count()
    # 记录成功用例数
    success=0
    # 记录失败用例数
    fail=0
    # 保存执行结果
    total_data=[]
    # 执行用例
    for execute_case_obj in execute_case_objs[:1]:
        pid=execute_case_obj.product_id
        mid=execute_case_obj.module_id
        id=execute_case_obj.id
        casename=execute_case_obj.apicase_name
        url=execute_case_obj.apicase_url
        method=execute_case_obj.apicase_method
        head=execute_case_obj.apicase_head
        requestdata=execute_case_obj.apicase_param
        relydata=execute_case_obj.apicase_relydata
        assertdata=execute_case_obj.apicase_assert
        needstore=execute_case_obj.apicase_needstore

        # 处理请求数据
        if '$' in requestdata:
            requestdata=request_data_handler(requestdata,tabObj=ApicaseInfo)
            print('请求数据：',requestdata)
        # 计时开始
        start_time=time.time()
        # 发请求
        res=api_request(url,method,eval(requestdata))
        # 耗时
        take_time=time.time()-start_time
        print(res.json())
        # 响应成功
        if res.status_code==200:
            # 断言
            if assertdata:
                assert_result=get_assert_result(eval(assertdata),res.json())
                print('断言结果：',assert_result)
            else:
                assert_result=''
            # 存储数据
            if needstore:
                store_data=get_store_data(eval(needstore),eval(requestdata),res.json())
                print('存储数据：',store_data)
            else:
                store_data=''
            # 写执行结果
            write_result(id,response=res.text[:50],result=assert_result,storedata='%s'%store_data,taketime='%s'%take_time,tabObj=ApicaseInfo)
            # 写bug
            if not assert_result:
                fail+=1
                bugname='%s，测试失败'%casename
                # detail='用例id：%s,请求地址：%s,请求方法：%s,请求数据：%s，响应结果：%s，断言：%s'%(id,url,method,requestdata,res.text[:50],assertdata)
                detail = '用例id：%s,请求数据：%s，响应结果：%s，断言：%s' % (id, requestdata, res.text[:10], assertdata)
                write_bug(pid=pid,mid=mid,name=bugname,detail=detail)
                total_data.append([url,requestdata,res.text,take_time,assertdata,'失败'])
            else:
                success+=1
                total_data.append([url, requestdata, res.text[:50], take_time, assertdata, '成功'])
        # 响应失败
        else:
            info('响应失败，响应码：%s,结果：%s'%(res.status_code,res.text))
        info('-'*50)

    # 写报告
    name='单接口测试报告'
    desc='接口每日扫描测试'
    file_name=time.strftime('%Y-%m-%d_%H-%M-%S')+'单接口测试报告'
    file_path=os.path.join(html_report_path,file_name)
    # 保存测试到html文件
    report_html(total_data,file_path)
    detail=file_name
    write_report(pid=pid,mid=mid,name=name,desc=desc,total=total,success=success,fail=fail,detail=detail)

    return HttpResponse('执行测试成功！')


# /apitest/apis/run/
from apitest.apis_utils import run_apis


def apis_run(request):
    run_apis()
    return HttpResponse('流程接口测试完成！')

