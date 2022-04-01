'''
get fitbit metrics view
'''


import logging

from django.views import View
from django.shortcuts import render

from main.globals import get_fitbit_link

class FitbitRegistration(View):
    '''
    return fitbit registration view
    '''
    template_name = "fitbit_registration.html"

    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        return render(request=request,
                      template_name=self.template_name,
                      context={"fitbit_link" : get_fitbit_link()})