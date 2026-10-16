'''
root path
'''
from django.shortcuts import render

def root_path(request):
    '''
    show the study welcome page for root path
    '''
    return render(request=request, template_name="fitbit_registration.html")
