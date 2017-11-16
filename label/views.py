# -*- encoding: utf8 -*-
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def get_home_page(request):
    '''
    return the home page contain a list of unlabeled queries.
    :param request:
    :return:
    '''


def index(request, a, b):
    return HttpResponse(int(a) + int(b))


def return_index(request):
    return render(request, 'home.html')
