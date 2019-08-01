from django.shortcuts import render

# Create your views here.

from product.models import ProductInfo
from module.models import ModuleInfo
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators import csrf
from django.core.paginator import Paginator
from commont.public_var import per_page_rows

# /module/index/
def module_index(request):
    """模块管理列表"""
    # 获取用户名
    username = request.session.get('user')
    # 获取所有模块
    # print('username:',username)
    modules = ModuleInfo.objects.all()
    # print('modules:',modules)
    # 统计模块数
    modules_count = ModuleInfo.objects.all().count()
    page = request.GET.get('page', '')
    # print('page:',page)
    # 分页
    paginator = Paginator(modules, per_page_rows)  # 每页显示数据的条数
    try:
        if page == '':
            page = 1
        else:
            page = int(page)
            if page > paginator.num_pages:
                page = paginator.num_pages
        page_modules = paginator.page(page)
        # print('page_modules:',page_modules)
        return render(request, 'module/module_index.html', {'modules': page_modules,
                                                              'username': username,
                                                              'modules_count': modules_count,
                                                              })
    except Exception as e:
        print('模块列表数据异常：', e)
        raise e


# /module/add/
def module_add(request):
    """模块添加"""
    return render(request,'module/module_add.html')


def get_product_names(request):
    """获取所有产品的名称"""
    products=ProductInfo.objects.all()
    if len(products):
        data=[]
        for product in products:
            data.append((product.id,product.product_name))
        return JsonResponse({'data':data})
    else:
        return JsonResponse({'data':'0'})


# /module/add_check/
@csrf.csrf_exempt
def add_check(request):
    """添加模块验证"""
    if request.method=="POST":
        # 获取请求数据
        product_id=request.POST.get('product_id')
        module_name=request.POST.get('module_name')
        module_desc=request.POST.get('module_desc')
        module_dev=request.POST.get('module_dev')
        module_tst=request.POST.get('module_tst')
        module_others=request.POST.get('module_others')
        if not product_id or product_id=='default':
            data={'code':'0','message':'请选择产品名称！'}
            return JsonResponse({'data':data})
        if not module_name:
            data={'code':'0','message':'模块名称不能为空'}
            return JsonResponse({'data':data})
        module_name_exists=ModuleInfo.objects.filter(module_name=module_name)
        print(module_name_exists)
        print('模块名称存在数量:',len(module_name_exists))
        if len(module_name_exists):
            data={'code':'0','message':'模块名称已存在'}
            return JsonResponse({'data':data})
        try:
            product=ProductInfo.objects.get(id=int(product_id))
            ModuleInfo.objects.create(product_id=product,
                                       module_name=module_name,
                                       module_desc=module_desc,
                                       module_dev=module_dev,
                                       module_tst=module_tst,
                                       module_others=module_others,
                                       create_time=datetime.now())
            data={'code':'1','message':'操作成功'}
            return JsonResponse({'data':data})
        except Exception as e:
            print('添加模块异常：',e)
            data={'code':'0','message':'未知错误：%s'%e}
            return JsonResponse({'data':data})
    else:
        data={'code':'0','message':'请求方式不正确'}
        return JsonResponse({'data':data})


# /module/search/
def module_search(request):
    """模块查找"""
    username = request.session.get('user')
    module_name = request.GET.get('module_name')
    modules = ModuleInfo.objects.filter(module_name=module_name)
    modules_count = modules.count()
    # page=request.GET.get('page','')
    print(len(modules))
    try:
        if len(modules):
            return render(request, 'module/module_index.html', {'username': username,
                                                                  'modules': modules,
                                                                  'modules_count': modules_count,
                                                                  })
        else:
            return render(request, 'module/module_index.html', {'username': username,
                                                                  'err_msg': '无数据',
                                                                  })
    except Exception as e:
        return render(request, 'module/module_index.html', {'username': username,
                                                            'err_msg': '查找出现异常！'
                                                            })


# /module/detail/{{mid}}
def module_detail(request,mid):
    """模块详情"""
    username = request.session.get('user')
    try:
        # 获取模块对象
        module = ModuleInfo.objects.get(id=mid)
        return render(request, 'module/module_detail.html', {'module':module})
    except Exception as e:
        print('查看模块详情异常：', e)
        return render(request,'module/module_detail.html',{'err_message':e})


# /module/change/{{mid}}
def module_change(request,mid):
    """产品修改页面"""
    username=request.session.get('user')
    try:
        # 获取模块信息
        module=ModuleInfo.objects.get(id=int(mid))
        return render(request, 'module/module_change.html', {'module':module})
    except Exception as e:
        print('修改产品异常：',e)
        return render(request, 'module/module_change.html', {'err_message':e})



# /module/change_check/
@csrf.csrf_exempt
def change_check(request):
    """修改产品验证"""
    if request.method == "POST":
        # 获取请求数据
        pid=request.POST.get('pid','')
        print('pid:',pid)
        mid=request.POST.get('mid','')
        module_name = request.POST.get('module_name','')
        module_desc = request.POST.get('module_desc')
        module_dev = request.POST.get('module_dev')
        module_tst=request.POST.get('module_tst')
        module_others = request.POST.get('module_others')
        if not pid or pid=='default':
            data={'code':'0','message':'请选择产品名称！'}
            return JsonResponse({'data':data})
        if not module_name:
            data = {'code': '0', 'message': '请输入模块名称'}
            return JsonResponse({'data': data})
        module_exists = ModuleInfo.objects.filter(module_name=module_name).exclude(id=mid)
        print(module_exists)
        print('产品名称存在数量:', len(module_exists))
        if len(module_exists):
            data = {'code': '0', 'message': '产品名称已存在'}
            return JsonResponse({'data': data})
        try:
            module=ModuleInfo.objects.get(id=int(mid))
            module.product_id=ProductInfo.objects.get(id=int(pid))
            module.module_name=module_name
            module.module_desc=module_desc
            module.module_dev=module_dev
            module.module_tst=module_tst
            module.module_others=module_others
            module.create_time=datetime.now()
            module.save()
            data = {'code': '1', 'message': '操作成功'}
            return JsonResponse({'data': data})
        except Exception as e:
            print('修改产品异常：', e)
            data = {'code': '0', 'message': '未知错误：%s' % e}
            return JsonResponse({'data': data})
    else:
        data = {'code': '0', 'message': '请求方式不正确'}
        return JsonResponse({'data': data})



# /module/delete/
@csrf.csrf_exempt
def module_delete(request):
    """删除模块"""
    if request.method=='POST':
        mid=request.POST.get('id')
        mname=request.POST.get('name')
        module_exists=ModuleInfo.objects.filter(id=mid,module_name=mname)
        if len(module_exists):
            module_exists.delete()
            data={'code':'1','message':'删除成功！'}
        else:
            data={'code':'0','message':'删除的数据不存在！'}
        return JsonResponse({'data':data})
    else:
        data={'code':'0','message':'请求方式不正确！'}
        return JsonResponse({'data':data})