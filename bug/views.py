from django.shortcuts import render

# Create your views here.

from bug.models import Bug
from commont.public_var import per_page_rows
from django.core.paginator import Paginator

# /bug/index/
def bug_index(request):
    """bug首页"""
    username = request.session.get('user')
    bugs = Bug.objects.all()
    bug_count = Bug.objects.all().count()
    page = request.GET.get('page', '')
    paginator = Paginator(bugs, per_page_rows)
    try:
        if page == '':
            page = 1
        else:
            page = int(page)
            if page > paginator.num_pages:
                page = paginator.num_pages
        bug_list = paginator.page(page)
        return render(request, 'bug/bug_index.html', {'username': username,
                                                            'bugs': bug_list,
                                                            'bug_count': bug_count
                                                            })
    except Exception as e:
        print('bug列表异常：', e)
        render(request, 'bug/bug_index.html', {'username': username, 'err_msg': 'bug列表异常，请稍后再试！'})


# /bug/search/
def bug_search(request):
    """报告查找"""
    username = request.session.get('user')
    name = request.GET.get('bug_name')
    bugs = Bug.objects.filter(name=name)
    bug_count=Bug.objects.filter(name=name).count()

    page = request.GET.get('page', '')
    paginator = Paginator(bugs, per_page_rows)

    try:
        if page == '':
            page = 1
        else:
            page = int(page)
            if page > paginator.num_pages:
                page = paginator.num_pages
        bug_list = paginator.page(page)
        return render(request, 'bug/bug_index.html', {'username': username,
                                                      'bugs': bug_list,
                                                      'bug_count': bug_count,
                                                      'bug_name':name
                                                      })
    except Exception as e:
        print('bug列表异常：', e)
        render(request, 'bug/bug_index.html', {'username': username, 'err_msg': 'bug列表异常，请稍后再试！'})

