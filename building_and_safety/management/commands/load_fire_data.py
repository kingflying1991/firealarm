import os
import csv
import logging
from datetime import datetime
from django.conf import settings
from django.contrib.gis.geos import Point
from building_and_safety.models import FireAlarm
from ast import literal_eval as make_tuple
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Load complaints filed to the city department of building and safety into the database."

    def parse_booleans(self, value):
        """
        Quick method to return True or False from the text values in the CSV
        """
        if value == "1":
            return True
        else:
            return False 

    def flush_fire_alarms(self):
        """
        Wipe all the complaints in the database.
        So we don't accidentally dupe ourselves. 
        """
        FireAlarm.objects.all().delete()

    def parse_int(self, s):
        """
        If the cell has a value, strip any possible extra spaces
        and return that value as an integer.
        """
        if s != None:
            try:
                s = s.strip()
                s = int(s)
            except ValueError, AttributeError:
                s = None
            return s
        else:
            return s

    def parse_float(self, s):
        """
        If the cell has a value, strip any possible extra spaces
        and return that value as an float number.
        """
        if s != None:
            try:
                s = s.strip()
                s = float(s)
            except ValueError, AttributeError:
                s = None
            return s
        else:
            return s
 
    def handle(self, *args, **options):
        """
        Load in our CSVs of fire alarms, 
        creating FireAlarm objects and adding them to a list
        which is then batch loaded into the database.

        We batch load them to keep from hitting the database for every record, 
        which would take approximately forever. 
        """
        self.data_dir = os.path.join(settings.ROOT_DIR, 'building_and_safety', 'data')
        logger.debug("flushing fire alarms")
        self.flush_fire_alarms()

        alarm_list = []

        # Our two CSVs of open and closed cases
        paths = ['fire_alarms_features_out.csv']

        for p in paths: 
            path = os.path.join(self.data_dir, p)
            reader = csv.DictReader(open(path, 'r'))
            for row in reader:
            	 #print self.parse_booleans(row["label"])
                c = FireAlarm(
                   instance_no = row["instance_no"],
                   alarm_code = row["alarm_code"],
                   building_type = row["building_type"],
                   repeat_cnt = self.parse_int(row["repeat_cnt"]),
                   activation_year = self.parse_int(row["activation_year"]),
                   activation_month = self.parse_int(row["activation_month"]),
                   activation_day = self.parse_int(row["activation_day"]),
                   activation_hour = self.parse_int(row["activation_hour"]),
                   time_of_the_day = self.parse_int(row["time_of_the_day"]),
                   day_of_week = self.parse_int(row["day_of_week"]),
                   in_holiday = self.parse_booleans(row['in_holiday']),
                   longtitude_x = self.parse_float(row["longtitude_x"]),
                   latitude_y = self.parse_float(row["latitude_y"]),
                   region = row['region'],
                   temperature = self.parse_float(row["temperature"]),
                   rainfall = self.parse_float(row["rainfall"]),
                   true_or_false_alarm = self.parse_booleans(row["label"])
                )
                 
                alarm_list.append(c)

        logger.debug("Loading fire alarms  to database.")

        # Batch upload our fire alarms to the database, 500 at a time
        FireAlarm.objects.bulk_create(
            alarm_list,
            batch_size=500
        )