from random import choice

import arrow
from django.http import HttpResponse
from django.shortcuts import render, redirect

from forms import *
from models import *


# Create your views here.
def shortener(request):
    if request.method == 'POST':
        form = URL_create(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            time = arrow.utcnow()
            url = ""
            url_list = Url.objects.filter().values('short_url')
            while url == "" or url in url_list:
                url = ""
                for i in range(6):
                    url += choice('1234567890abcdef')
            Url.objects.create(url=data['url'], cr_time=time.format('YYYY - MM - DD HH:mm:ss'), short_url=url)
            return HttpResponse("You've been create short URL")
        context = {'my_form': form}
        return render(request, 'my_form.html', context)
    elif request.method == 'GET':
        shr = request.GET.get('shr')
        data = Url.objects.filter(short_url=shr).get()
        Url.objects.filter(short_url=shr).update(clicks = data.clicks+1)
        return redirect(data.url)
    else:
        context = {'my_form': URL_create()}
        return render(request, 'my_form.html', context)


def url_list(request):
    data = Url.objects.filter()
    context = {'data': data}
    return render(request, 'list.html', context)
