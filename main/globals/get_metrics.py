'''
get fitbit metrics
'''
from multiprocessing import Pool

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
    logger = logging.getLogger(__name__)

    result = {}
    status = 'success'
    message = 'metrics pulled successfully'

    try:
        fitbit_user = FitBitUser.objects.get(user_id=fitbit_user_id)
    except ObjectDoesNotExist :
        logger = logging.getLogger(__name__)     
        logger.error(f"get_metrics_from_dict: user not found {fitbit_user_id}")
        status = "fail"
        message = 'user not found'

    if status == 'success':

        if fitbit_user.check_need_to_refresh_access_token():
            v = fitbit_user.refresh_access_token()        
            status = v['status']
            message = v['message']

        #single thred pull
        # for i in fitbit_metrics_dict:        
        #     result[i] = get_metric(fitbit_metrics_dict[i], fitbit_user)

        #     if result[i]["status"] == "fail":
        #         message = result[i]["status"]
        #         break

        #multi thred pull
        if status == "success":
            try:
                with Pool(len(fitbit_metrics_dict)) as p:
                    
                    result = {i:p.apply_async(func=get_metric,args=(fitbit_metrics_dict[i], fitbit_user)) for i in fitbit_metrics_dict}

                    for i in result:
                        result[i] = result[i].get()
            except Exception as error:
                logger.error(f"get_metrics_from_dict: {error}")
                status = "fail"
                message = "pull failed"

    return {'status':status, 'message':message, 'result':result}

  #take fitbit api url and return response
def get_metric(url, fitbit_user):
    logger = logging.getLogger(__name__)        

    r = get_metric_2(url, fitbit_user)

    status = "success"
    message = ""
    
    #try to reauthorize
    if type(r) == dict and r.get('success', 'not found') == False:        
        
        #v = fitbit_user.refresh_access_token()

        status = "fail"
        message = "pull failed"


        # if v["status"] == "success":
        #     r = get_metric_2(url, fitbit_user)
        # else:
        #     message = v["message"]
    
    return {'status':status, 'message': message, 'result' : r}

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

