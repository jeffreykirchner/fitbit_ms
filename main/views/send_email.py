'''
send email view
'''
from datetime import datetime

import logging
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from django.conf import settings

#from main.globals import send_mass_email_from_template
from main.globals import send_mass_email_message_from_template

class SendEmailView(APIView):
    '''
    take a mass email for sending
    '''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        '''
        handle incoming send mass email
        '''
        logger = logging.getLogger(__name__)
        logger.info(request.data)

        result = take_and_send_incoming_email(request.user, request.data, settings.DEBUG)

        return Response(result['text'], status=result['code'])

def take_and_send_incoming_email(user, data, use_test_subject):
    '''
    take incoming email and send it, send emails in groups of block size to limit overloading
    '''

    email_block = 250
    result_list = []
    email_counter = 0
    user_list = []
    sleep_length = 61

    for u in data["user_list"]:

        email_counter += 1
        user_list.append(u)

        #if email counter hits block size, send emails then pause for cool down
        if email_counter == email_block:
            
            time_start = datetime.now()      
        
            
            result_list.append(send_mass_email_message_from_template(user,
                                                user_list,
                                                data["message_subject"],
                                                data["message_text"],
                                                data.get("message_text_html", None),
                                                data["memo"],
                                                use_test_subject))

            time_end = datetime.now()
            time_span = time_end-time_start

            email_counter = 0
            user_list = []
            time.sleep(sleep_length-time_span.total_seconds())

    # if len(data["user_list"]) >= email_block:
    #     time.sleep(sleep_length)

    #send remaining partial email block
    if len(user_list) > 0:
        result_list.append(send_mass_email_message_from_template(user,
                                                        user_list,
                                                        data["message_subject"],
                                                        data["message_text"],
                                                        data.get("message_text_html", None),
                                                        data["memo"],
                                                        use_test_subject))

    mail_count = 0
    mail_code = status.HTTP_201_CREATED
    error_message = ""

    for r in result_list:
        mail_count += r["text"]["mail_count"]

        if r["text"]["error_message"] != "":
            error_message += r["text"]["error_message"] + " "
        
        if r["code"] == status.HTTP_400_BAD_REQUEST:
            mail_code = status.HTTP_400_BAD_REQUEST
        
    return {'text' : {"mail_count" : mail_count, "error_message" : error_message},
            'code' : mail_code}