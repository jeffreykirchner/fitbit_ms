'''
privacy policy page
'''
from django.shortcuts import render

def privacy_policy(request):
    '''
    show the privacy policy
    '''
    return render(request=request, template_name="privacy_policy.html")
