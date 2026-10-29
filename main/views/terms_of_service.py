'''
Terms of Service page
'''
from django.shortcuts import render


def terms_of_service(request):
    '''
    show the Terms of Service
    '''
    return render(request=request, template_name="terms_of_service.html")
