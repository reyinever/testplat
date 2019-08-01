from django.shortcuts import render

# Create your views here.

from report.models import Report
from commont.public_var import per_page_rows
from django.core.paginator import Paginator


# /report/index/
def report_index(request):
    """报告列表"""
    username = request.session.get('user')
    reports = Report.objects.all()
    report_count = Report.objects.all().count()
    page = request.GET.get('page', '')
    paginator = Paginator(reports, per_page_rows)
    try:
        if page == '':
            page = 1
        else:
            page = int(page)
            if page > paginator.num_pages:
                page = paginator.num_pages
        report_list = paginator.page(page)
        return render(request, 'report/report_index.html', {'username': username,
                                                        'reports': report_list,
                                                        'report_count': report_count
                                                        })
    except Exception as e:
        print('报告列表异常：', e)
        render(request, 'report/report_index.html', {'username': username, 'err_msg': '用例列表异常，请稍后再试！'})


# /report/testReport/'+filename+'.html'
def report_detail(request,filename):
    """html详情页面"""
    return render(request,'report/testReport/'+filename+'.html')


# /report/search/
def report_search(request):
    """报告查找"""
    username = request.session.get('user')
    name = request.GET.get('report_name')
    reports = Report.objects.filter(name=name)

    report_count=Report.objects.filter(name=name).count()

    if len(reports):
        return render(request, 'report/report_index.html', {'username': username, 'reports': reports,'report_count': report_count})
    else:
        return render(request, 'report/report_index.html', {'username': username, 'err_msg': '无数据'})

