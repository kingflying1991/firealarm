import json
import logging
import calculate
from datetime import datetime
from django.db import models
from django.db.models import Avg
from django.utils import dateformat

import usaddress
from lifelines import KaplanMeierFitter

logger = logging.getLogger(__name__)

class FireAlarm(models.Model):
    instance_number = models.CharField(max_length=20, db_index=True, help_text='False alarms instance number')
    creation_date = models.DateTimeField(blank=True,null=True)
    activation_date = models.DateTimeField(blank=True,null=True)
    alarm_code = models.CharField(max_length=20,blank=True,null=True)
    incd_address = models.CharField(max_length=1024,blank=True,null=True)
    np_id = models.IntegerField(blank=True,null=True)
    alarm_type = models.CharField(max_length=20,blank=True,null=True)
    incident_type = models.CharField(max_length=50,blank=True,null=True)
    call_source = models.CharField(max_length=20,blank=True,null=True)
    repeat_count = models.IntegerField(blank=True,null=True)
    x = models.FloatField(blank=True,null=True)
    y = models.FloatField(blank=True,null=True)

    # Extract fields
    year = models.IntegerField(blank=True,null=True)
    month = models.IntegerField(blank=True,null=True)
    region  = models.CharField(max_length=20,blank=True,null=True)

    objects = models.Manager()

    class Meta:
        ordering = ("-creation_date",)

    def __str__(self):
        return self.instance_number

    def __unicode__(self):
        return unicode(self.instance_number)

    def get_date_in_detail(self):
        if(self.activation_date):
            self.year = self.activation_date.year
            self.month = self.activation_date.month

    def get_region(self):
        if(self.incd_address):
            try:
                tag = usaddress.tag(self.incd_address)[0]
                if(tag.has_key('PlaceName')):
                    places = tag['PlaceName'].split(",")
                    if(len(places) >= 1):
                        self.region = places[len(places) - 1].strip()
            except usaddress.RepeatedLabelError:
                self.region = None

class FireAlarmFeature(models.Model):
    """
    The feature of false alarms of NSW, Australia
    """
    instance_number = models.CharField(max_length=20, db_index=True, help_text='False alarms instance number')

    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)

    time_of_the_day = models.CharField(max_length=20,blank=True, null=True)
    raw_time_of_the_day = models.CharField(max_length=20,blank=True, null=True)
    day_of_week = models.CharField(max_length=20, blank=True, null=True)
    raw_day_of_week = models.CharField(max_length=20, blank=True, null=True)

    season = models.CharField(max_length=20, blank=True, null=True)
    in_holiday = models.NullBooleanField(default=False)

    alarm_type = models.IntegerField(blank=True,null=True)
    incident_type = models.IntegerField(blank=True,null=True)
    alarm_code = models.CharField(max_length=10, blank=True, null=True)

    repeat_count  = models.IntegerField(blank=True, null=True)
    building_type = models.CharField(max_length=20, blank=True, null=True)

    region = models.CharField(max_length=10, blank=True, null=True)
    longtitude_x = models.FloatField(null=True,blank=True)
    latitude_y = models.FloatField(null=True,blank=True)

    temperature = models.FloatField(blank=True, null=True)
    rainfall = models.FloatField(blank=True, null=True)

    true_or_false_alarm = models.BooleanField(blank=False, null=False,default=False)

    # Managers
    objects = models.Manager()

    class Meta:
        ordering = ("-year", "-month", "-day", "-hour")

    def __str__(self):
        return self.instance_number

    def __unicode__(self):
        return unicode(self.csr)

    def get_activate_date(self):
        return "-".join([str(self.year), str(self.month), str(self.day)])

    def as_geojson_dict(self):
        """
        Method to return each feature in the DB as a geojson object.
        """
        as_dict = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(self.longtitude_x),
                    float(self.latitude_y)
                ]
            },
            "properties": {
                "instance_no": self.instance_no,
                "date": self.get_activate_date(),
                "building_type": self.building_type
            }
        }
        return as_dict

class Features(models.Model):
    feature_name = models.CharField(max_length=20, db_index=True, help_text='Feature name')
    feature_desc = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.feature_name

class DataCube(models.Model):
    features = models.CharField(max_length=50, help_text='The feature combinations')
    true_alarm = models.IntegerField(null=True, blank=True)
    false_alarm = models.IntegerField(null=True, blank=True)
    per_true_alarm = models.FloatField(null=True, blank=True)
    per_false_alarm = models.FloatField(null=True, blank=True)
