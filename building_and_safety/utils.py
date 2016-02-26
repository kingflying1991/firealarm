import django_tables2 as tables
from building_and_safety.models import DataCube

class Utils:
    @staticmethod
    def parse_int(s):
        if s != None:
            try:
                s = s.strip()
                s = int(s)
            except ValueError, AttributeError:
                s = None
            return s
        else:
            return s

    @staticmethod
    def parse_float(s):
        if s != None:
            try:
                s = s.strip()
                s = float(s)
            except ValueError, AttributeError:
                s = None
            return s
        else:
            return s

class DataCubeTable(tables.Table):
    features = tables.Column()
    true_alarm = tables.Column()
    false_alarm = tables.Column()
    per_true_alarm = tables.Column()
    per_false_alarm = tables.Column()

    class Meta:
        attrs = {"class": "paleblue"}