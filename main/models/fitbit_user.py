'''
fitbit user model
'''

from django.db import models

class FitBitUser(models.Model):
    '''
    fitbit user model
    '''
    user_id = models.CharField(max_length=100, default="",verbose_name = 'FitBit User ID')  

    access_token = models.CharField(max_length=1000, default="", verbose_name = 'FitBit Access Token')
    refresh_token = models.CharField(max_length=1000, default="", verbose_name = 'FitBit Refresh Token')

    last_synced =  models.DateTimeField(default=None, null=True, verbose_name = 'FitBit Last Synced')
    time_zone = models.CharField(max_length=1000, default="", verbose_name = 'FitBit Time Zone')

    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        verbose_name = 'Fitbit User'
        verbose_name_plural = 'Fitbit Users'

