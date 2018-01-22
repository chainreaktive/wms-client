from django.contrib.auth.models import User
import requests
from .local_settings import MOCA_URL, WH_ID
from mocanexion import *

class MocaBackend(object):

    supports_inactive_user = False

    def authenticate(self, request, username=None, password=None, devcod=None, wh_id = WH_ID, url = MOCA_URL):

        moca = MocaNexion()

        try:
            moca.connect(url, username, password, devcod, wh_id)
            request.session['moca'] = moca

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username, password=password)
                user.save()

            return user

        except:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
