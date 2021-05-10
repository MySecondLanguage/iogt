from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from home.models import Article, Comment
from django.http import HttpResponseRedirect

@login_required
def page_comment(request, pk):
    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')
        Comment.objects.create(
            page=Article.objects.get(pk=pk),
            comment=request.POST['comment'],
            author=request.user,
            ip_address=ipaddress
        )
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def reply_comment(request, pk):
    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')
        Comment.objects.create(
            page=Comment.objects.get(pk=pk).page,
            comment=request.POST['comment'],
            author=request.user,
            ip_address=ipaddress,
            parent=Comment.objects.get(pk=pk)
        )
    return HttpResponseRedirect(request.META['HTTP_REFERER'])