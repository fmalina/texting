"""
Generic pagination reusable at view level.

Paging middleware needs installing in the settings:

    MIDDLEWARE_CLASSES = (
        ... almost at the end...
        'paging.PagingMiddleware',

Use in a view like so:

    from paging import simple_paging
    
    def listings(request):
        ls = Listing.objects.all()
        ls, count, paging = simple_paging(request, ls, 100)
        return render(request, 'some_listings.html', {
            'ls': ls, 'count': count, 'paging': paging
            })

Include paging in your listings template:
    
    {{ paging }}

"""
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect


class PagingMiddleware(object):
    def process_request(self, request):
        try:
            request.page = int(request.GET.get('page', 1))
        except ValueError: # redirect invalid page numbers to root page
            return HttpResponseRedirect(request.path)

def simple_paging(request, qs, limit, custom_render=False):
    pager = Paginator(qs, limit)
    try: 
        page_obj = pager.page(request.page)
        qs = page_obj.object_list
    except EmptyPage:
        page_obj = {}
        qs = qs.none()
    
    pages = pager.page_range
    count = pager.count
    
    if custom_render:
        return qs, count, pages
    
    paginate = render_paging(request, pages, page_obj, count, limit)
    
    return qs, count, paginate

def render_paging(request, pages, page_obj, count, limit):
    pages = sample(pages, request.page)
    
    get = request.GET.copy()
    get.pop('page', None)
    
    return render_to_string('pagination.html', {
        'path': request.path_info,
        'mobile': bool(getattr(request, 'mobile', 0)),
        'pages': pages,
        'page_obj': page_obj,
        'is_paginated': count > limit,
        'getvars': '&' + get.urlencode() if get else ''
    })

def sample(pages, current):
    '''Show first few, few around the current page & a last page'''
    if len(pages) > 20:
        ls = []
        prev = False
        for x in pages:
            a = False
            if x in range(1,5)\
            or x in range(current-5, current+5)\
            or x == pages[-1]:
                a = x
            if prev or a:
                ls.append(a)
            prev = a
        pages = ls
    return pages