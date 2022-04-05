'''
get fitbit metrics view
'''

from rest_framework.views import APIView
from rest_framework import permissions

import logging

from rest_framework.response import Response

from main.globals import get_metrics_from_dict

class GetMetrics(APIView):
    '''
    return dict of fitbit metrics
    '''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        '''
        return dic of fitbit metrics
        '''
        logger = logging.getLogger(__name__)


        logger.info(request.data)

        fitbit_user = request.data.get("fitbit_user")
        metrics_dict = request.data.get("metrics_dict")

        logger.info(f"Get Metrics: user {fitbit_user}, metrics {metrics_dict} ")

        return Response(get_metrics_from_dict(fitbit_user, metrics_dict))