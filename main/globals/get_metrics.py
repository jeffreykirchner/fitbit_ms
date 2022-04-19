'''
get fitbit metrics
'''
import urllib
import logging
import requests

from django.core.exceptions import ObjectDoesNotExist

from main.models import Parameters
from main.models import FitBitUser

from django.conf import settings

def get_metrics_from_dict(fitbit_user_id, fitbit_metrics_dict):
    '''
    take a list dict of fitbit metrics to pull and return dict with responses
    '''
    result = {}

    try:
        fitbit_user = FitBitUser.objects.get(user_id=fitbit_user_id)
    except ObjectDoesNotExist :
        logger = logging.getLogger(__name__)     
        logger.error(f"get_metrics_from_dict: user not found {fitbit_user_id}")
        return {"error" : f'user not found {fitbit_user_id}'}

    for i in fitbit_metrics_dict:        
        result[i] = get_metric(fitbit_metrics_dict[i], fitbit_user)

    return result

  #take fitbit api url and return response
def get_metric(url, fitbit_user):
    logger = logging.getLogger(__name__)        

    r = get_metric_2(url, fitbit_user)

    status = "success"
    message = ""
    
    #try to reauthorize
    if type(r) == dict and not r.get('success', False):        
        headers = {'Authorization': 'Basic ' + str(settings.FITBIT_AUTHORIZATION) ,
                   'Content-Type' : 'application/x-www-form-urlencoded'}
        
        data = {'grant_type' : 'refresh_token',
                'refresh_token' : fitbit_user.refresh_token}    
        
        r = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data).json()

        if 'access_token' in r:
            fitbit_user.access_token = r['access_token']
            fitbit_user.refresh_token = r['refresh_token']

            fitbit_user.save()

            logger.info("Fitbit refresh: User " + str(fitbit_user.user_id))
            logger.info(r)
        else:
            logger.warning(f"Fitbit refresh failed: {r}")
            status = "fail"
            for e in r['errors']:
                if e['errorType'] == 'invalid_grant':
                    message = "re-connect required"

        if status == "success":
            r = get_metric_2(url, fitbit_user)
    
    return {'status':status, 'message' : message, 'result' : r}

def get_metric_2(url, fitbit_user):
    '''
    try to pull metric
    '''
    logger = logging.getLogger(__name__)     

    headers = {'Authorization': 'Bearer ' + fitbit_user.access_token,
               'Accept-Language' :	'en_US'}    

    try:            
        r = requests.get(url, headers=headers)

        r = r.json()

        logger.info(f"Fitbit request: {url} ")
        logger.info(f"Fitbit request: {r}")

        return r
    except Exception as e: 
        logger.warning(f"get_metric_2 error: {e} , response: {r}")
        return  "fail"

def get_fitbit_link(temp_state):
    p = Parameters.objects.first()

    #link to setup fitbit
    tempURL = p.site_URL+"fitbit-registration-response/"
    tempURL = tempURL.replace(":","%3A")
    tempURL = tempURL.replace("/","%2F")

    tempClientID = settings.FITBIT_CLIENT_ID
    tempState = temp_state
    fitBit_Link = f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={tempClientID}&redirect_uri={tempURL}&scope=activity%20heartrate%20sleep%20settings%20profile%20weight&expires_in=604800&prompt=login%20consent&state={tempState}"

    return fitBit_Link

