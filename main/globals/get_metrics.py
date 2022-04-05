'''
get fitbit metrics
'''
import urllib

from main.models import Parameters
from django.conf import settings

def get_metrics_from_dict(fitbit_user, fitbit_metrics_dict):
    '''
    take a list dict of fitbit metrics to pull and return dict with responses
    '''


    return {}

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

