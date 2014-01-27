# -*- coding: utf-8 -*-

"""
    Front app
    Author  :   Alvaro Lizama Molina <alvaro@knoudo.com>
"""

from django.shortcuts import render


def index(request):
    """
        Index
    """
    return render(request, 'index.html', {})
