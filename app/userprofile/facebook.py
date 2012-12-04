from django.conf import settings

import urllib


class Facebook(object):
    params = {'fb_id': settings.FACEBOOK_APPS_ID}

    def