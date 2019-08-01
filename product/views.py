from django.shortcuts import render

# Create your views here.

from product.models import ProductInfo
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django.views.decorators import csrf
from django.core.paginator import Paginator
from django.shortcuts import redirect
from commont.public_var import per_page_rows


# /product/index/
def index(request):
    """产品信息页"""
    # 获取用户名
    username=request.session.get('user')
    # 获取所有产品
    products=ProductInfo.objects.all()
    # 统计产品数
    products_count=ProductInfo.objects.all().count()
    page=request.GET.get('page','')
    # 分页
    paginator=Paginator(products,per_page_rows)  # 每页显示数据的条数
    try:
        if page=='':
            page=1
        else:
            page=int(page)
            if page>paginator.num_pages:
                page=paginator.num_pages
        products = paginator.page(page)
        return render(request, 'product/product_index.html', {'products': products,
                                                       'username': username,
                                                       'products_count': products_count,
                                                       })
    except Exception as e:
        print('产品列表数据异常：',e)
        raise e


def product_search(request):
    """产品查找"""
    username=request.session.get('user')
    product_name=request.GET.get('product_name')
    products=ProductInfo.objects.filter(product_name=product_name)
    products_count=products.count()
    # page=request.GET.get('page','')
    print(len(products))
    try:
        if len(products):
            return render(request,'product/product_index.html',{'username':username,
                                                                'products':products,
                                                                'products_count':products_count,
                                                                })
        else:
            return render(request,'product/product_index.html',{'username':username,
                                                                'err_msg':'无数据',
                                                                })
    except Exception as e:
        return render(request,'product/product_index.html',{'username':username,
                                                            'err_msg': '查找出现异常！',
                                                            })


# /product/add/
def product_add(request):
    """新增产品"""
    return render(request,'product/product_add.html')


# /product/add_check
@csrf.csrf_exempt
def add_check(request):
    """新增产品验证"""
    if request.method=="POST":
        # 获取请求数据
        product_name=request.POST.get('product_name')
        product_desc=request.POST.get('product_desc')
        product_manager=request.POST.get('product_manager')
        product_others=request.POST.get('product_others')
        if not product_name or not product_manager:
            data={'code':'0','message':'有必填项未填写'}
            return JsonResponse({'data':data})
        product_name_exists=ProductInfo.objects.filter(product_name=product_name)
        print(product_name_exists)
        print('产品名称存在数量:',len(product_name_exists))
        if len(product_name_exists):
            data={'code':'0','message':'产品名称已存在'}
            return JsonResponse({'data':data})
        try:
            ProductInfo.objects.create(product_name=product_name,
                                       product_desc=product_desc,
                                       product_manager=product_manager,
                                       product_others=product_others,
                                       create_time=datetime.now())
            data={'code':'1','message':'操作成功'}
            return JsonResponse({'data':data})
        except Exception as e:
            print('添加产品异常：',e)
            data={'code':'0','message':'未知错误：%s'%e}
            return JsonResponse({'data':data})
    else:
        data={'code':'0','message':'请求方式不正确'}
        return JsonResponse({'data':data})


# /product/change/{{pid}}
def product_change(request,pid):
    """产品修改页面"""
    username=request.session.get('user')
    try:
        # 获取产品信息
        product=ProductInfo.objects.get(id=pid)
        product_name=product.product_name
        product_desc=product.product_desc
        product_manager=product.product_manager
        product_others=product.product_others
        return render(request, 'product/product_change.html', {'id':pid,
                                                               'username': username,
                                                               'product_name': product_name,
                                                               'product_desc':product_desc,
                                                               'product_manager':product_manager,
                                                               'product_others':product_others
                                                               })
    except Exception as e:
        print('修改产品异常：',e)

@csrf.csrf_exempt
def change_check(request):
    """修改产品验证"""
    if request.method == "POST":
        # 获取请求数据
        pid=request.POST.get('pid')
        product_name = request.POST.get('product_name')
        product_desc = request.POST.get('product_desc')
        product_manager = request.POST.get('product_manager')
        product_others = request.POST.get('product_others')
        if not product_name or not product_manager:
            data = {'code': '0', 'message': '有必填项未填写'}
            return JsonResponse({'data': data})
        product_exists = ProductInfo.objects.filter(product_name=product_name).exclude(id=pid)
        print(product_exists)
        print('产品名称存在数量:', len(product_exists))
        if len(product_exists):
            data = {'code': '0', 'message': '产品名称已存在'}
            return JsonResponse({'data': data})
        try:
            product=ProductInfo.objects.get(id=int(pid))
            product.product_name=product_name
            product.product_desc=product_desc
            product.product_manager=product_manager
            product.product_others=product_others
            product.create_time=datetime.now()
            product.save()
            data = {'code': '1', 'message': '操作成功'}
            return JsonResponse({'data': data})
        except Exception as e:
            print('修改产品异常：', e)
            data = {'code': '0', 'message': '未知错误：%s' % e}
            return JsonResponse({'data': data})
    else:
        data = {'code': '0', 'message': '请求方式不正确'}
        return JsonResponse({'data': data})


@csrf.csrf_exempt
def product_delete(request):
    if request.method=='POST':
        pid=request.POST.get('pid')
        pname=request.POST.get('pname')
        product_exists=ProductInfo.objects.filter(id=pid,product_name=pname)
        if len(product_exists):
            product_exists.delete()
            data={'code':'1','message':'删除成功！'}
        else:
            data={'code':'0','message':'删除的数据不存在！'}
        return JsonResponse({'data':data})
    else:
        data={'code':'0','message':'请求方式不正确！'}
        return JsonResponse({'data':data})


def product_detail(request,pid):
    username=request.session.get('user')
    try:
        # 获取产品信息
        product=ProductInfo.objects.get(id=pid)
        product_name=product.product_name
        product_desc=product.product_desc
        product_manager=product.product_manager
        product_others=product.product_others
        return render(request, 'product/product_detail.html', {'id': pid,
                                                               'username': username,
                                                               'product_name': product_name,
                                                               'product_desc':product_desc,
                                                               'product_manager':product_manager,
                                                               'product_others':product_others
                                                               })
    except Exception as e:
        print('查看模块详情异常：',e)




