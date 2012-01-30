# coding: utf-8

import datetime

def expiration_datetime(expiration_period):
    return (datetime.datetime.now() + datetime.timedelta(days=expiration_period))