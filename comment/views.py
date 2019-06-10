# import json
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
# from django.core.serializers import serialize
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm

def save_comment(request):
    refere = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        save_update = 0

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            save_update = 1
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        comment.send_mail()
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nikename_or_username()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['save_update'] = save_update
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nikename_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
        # data['comment'] = json.loads(serialize('json', [comment])[1:-1])
    else:
        data['status'] = 'ERROR'
        data['info'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)