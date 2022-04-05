'''
 fitbit regisitration request
'''

from django.db import models

class RegistrationRequest(models.Model):
    '''
    fitbit regisitration request
    '''
    return_url = models.CharField(max_length=1000, default="",verbose_name = 'Return URL')     #after registration request, return to this URL

    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Registration Request'
        verbose_name_plural = 'Registration Requests'

