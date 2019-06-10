import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse
from read_count.utils import get_weeks_read, get_today_data, get_yester_data
from blog.models import Blog

def get_weeks_data():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date).values('pk', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_weeks_read(blog_content_type)

    # 获得7天热门博客的缓存数据
    weeks_data = cache.get('weeks_data')
    if weeks_data is None:
        weeks_data = get_weeks_data()
        cache.set('weeks_data', weeks_data, 3600)

    today_data = get_today_data(blog_content_type)
    yester_data = get_yester_data(blog_content_type)
    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_data'] = today_data
    context['yester_data'] = yester_data
    context['weeks_data'] = weeks_data
    return render(request, 'home.html', context)