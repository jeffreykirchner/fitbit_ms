'''
get fitbit metrics view
'''


import logging
import json
import requests
import traceback

from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings

from main.globals import get_fitbit_link

from main.models import RegistrationRequest
from main.models import Parameters
from main.models import FitBitUser

class FitbitRegistrationResponse(View):
    '''
    return fitbit registration view
    '''
    template_name = "fitbit_registration_response.html"

    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        ''' 
        logger = logging.getLogger(__name__)

        status="success"

        p = Parameters.objects.first()

        fitBit_response = ""
        fitBit_error = ""

        if not "code" in request.GET:
            status="fail"
        else:

            try:
                logger.info("Register Fitbit, Code: " + request.GET["code"]) 
                logger.info("Register Fitbit, State: " + request.GET["state"]) 

                state_info = request.GET["state"].split(";")
                registration_request_id = state_info[0]

                registration_request = RegistrationRequest.objects.get(id=registration_request_id)

                headers = {'Authorization': 'Basic ' + str(settings.FITBIT_AUTHORIZATION),
                           'Content-Type' : 'application/x-www-form-urlencoded'}
                
                data = {'clientId': str(settings.FITBIT_CLIENT_ID),
                        'code': request.GET["code"], 
                        'redirect_uri' : f'{p.site_URL}fitbit-registration-response/',
                        'grant_type' : 'authorization_code'}

                fitBit_response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers,data=data).json()

                logger.info("Register Fitbit, Response: ") 
                logger.info(fitBit_response)

                if 'access_token' in fitBit_response:

                    fitbit_user, created = FitBitUser.objects.get_or_create(user_id=fitBit_response['user_id'])

                    fitbit_user.access_token = fitBit_response['access_token']
                    fitbit_user.refresh_token = fitBit_response['refresh_token']

                    fitbit_user.save()
                else:
                    status="fail"        
            
            except Exception as e:
                fitBit_error = str(e)
                logger.error("fitBit registration: " + fitBit_error)
                logger.error(traceback.format_exc())
                status="fail"
        
        logger.info("Register Fitbit, Status: " + status) 

        if status == "success":
            return redirect("http://" + registration_request.return_url.replace("user_id", fitbit_user.user_id))
        else:
            pass
        
        
