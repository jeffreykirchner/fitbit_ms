'''
get fitbit metrics view
'''


import logging
import json

from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect

from main.globals import get_fitbit_link

from main.models import RegistrationRequest

class FitbitRegistration(View):
    '''
    return fitbit registration view
    '''
    template_name = "fitbit_registration.html"

    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''
        logger = logging.getLogger(__name__)         
        
        try:
            
            r = RegistrationRequest()
            r.return_url = kwargs["return_url"]
            r.save()
            
        except Exception as e:
            logger.warning(f"Registration failed: {e}")
            return render(request=request,
                          template_name=self.template_name,
                          context={})
        
        return redirect(get_fitbit_link(r.id))
