'''
fitbit user model
'''
from datetime import datetime, timedelta

import requests
import logging
import pytz

from django.db import models
from django.conf import settings

class FitBitUser(models.Model):
    '''
    fitbit user model
    '''
    user_id = models.CharField(max_length=100, default="", verbose_name = 'FitBit User ID')  

    access_token = models.CharField(max_length=1000, default="", verbose_name = 'FitBit Access Token')
    refresh_token = models.CharField(max_length=1000, default="", verbose_name = 'FitBit Refresh Token')

    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        verbose_name = 'Fitbit User'
        verbose_name_plural = 'Fitbit Users'
    
    def refresh_access_token(self):
        '''
        refresh fitbit api access token
        '''
        logger = logging.getLogger(__name__)

        status = "success"
        message = ""

        headers = {'Authorization': 'Basic ' + str(settings.FITBIT_AUTHORIZATION) ,
                'Content-Type' : 'application/x-www-form-urlencoded'}
            
        data = {'grant_type' : 'refresh_token',
                'refresh_token' : self.refresh_token}    
        
        r = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data).json()

        if 'access_token' in r:
            self.access_token = r['access_token']
            self.refresh_token = r['refresh_token']

            self.save()

            logger.info(f"Fitbit refresh: User {self.user_id}, token {r}")

            status = "success"
        else:
            logger.warning(f"Fitbit refresh failed: {r}")
            status = "fail"
            for e in r['errors']:
                if e['errorType'] == 'invalid_grant':
                    message = "re-connect required"

        return {"status":status, "message":""}

    def check_need_to_refresh_access_token(self):
        '''
        check if 7 hours has passed and access token needs refresh
        '''

        if datetime.now(pytz.UTC) - self.updated > timedelta(hours=7):
            return True
        
        return False

