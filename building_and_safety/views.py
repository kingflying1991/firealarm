import json
import csv
import calculate
import collections
import logging
import os
from datetime import datetime

from django.db.models import Count
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.conf import settings
import django_tables2 as tables
from django_tables2   import RequestConfig

from building_and_safety.utils import Utils, DataCubeTable
from building_and_safety.models import FireAlarm, DataCube, Features

from django.http import HttpResponse

from .form import FireAlarmForm


logger = logging.getLogger(__name__)



#added by xiang
LABEL_TRUE = "true"
LABEL_FALSE = "false"
TYPE_NUMERIC = 0
TYPE_CATEGORY = 1
FEATURE_TYPE_MAP = {
"year":[0,2012,2015,1],
"month":[0,1,12,1],
"day":[0,1,31,1],
"hour":[0,0,23,1],
"time_of_day":[1],
"day_of_week":[0,0,6,1],
"incident_type":[1],
"alarm_code":[1],
"alarm_type":[1],
"repeat_count":[0,0,45,2],
"temperature":[0,-7,48,1],
"rainfall":[0,0,200,5],
"building_type":[1]
}



@csrf_exempt
def get_features(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        selected_feature_list = request.POST.getlist('features')
        return HttpResponseRedirect(reverse('get_data_cubes', args=("-".join(sorted(selected_feature_list)),)))
    else:
        #logger.debug("Got features: " + ",".join(str(i) for i in Features.objects.all()))
        return render(request, 'features.html', {'features': Features.objects.all()})



def get_data_cubes2(request, feature_file_name=''):
    data_dir = os.path.join(settings.ROOT_DIR, 'building_and_safety', 'data', 'Cube', feature_file_name + ".csv")
    logger.debug("data_dir: "+ data_dir)
    data_cube = []
    feature_list = sorted(feature_file_name.split('-'))
    #print "feature_list:", feature_list

    try:
        infile = open(data_dir, 'r')
        reader = csv.DictReader(infile)
        for row in reader:
            feature_combs = ''
            for f in feature_list:
                feature_combs += row[f] + " / "
            data_cube.append({
                'features' : feature_combs.rstrip(' / '),
                'true_alarm' :  Utils.parse_int(row['true_alarm']),
                'false_alarm' :  Utils.parse_int(row['false_alarm']),
                'per_true_alarm' : Utils.parse_float(row['true_percentage']),
                'per_false_alarm' : Utils.parse_float(row['false_percentage'])
                })
        infile.close()
        table = DataCubeTable(data_cube)
        RequestConfig(request, paginate={"per_page": 25}).configure(table)

        return_data = drawPiechartSingle(feature_file_name, data_cube)
        return_data['data_cube'] = table
        return_data['feature_name'] = feature_file_name
        #print return_data
        #print data_cube

        return render(request, 'fire_alarm_analysis2.html', return_data)
    except IOError:
        raise Http404("Feature combinations does not support")



class FireAlarmAnalysis(TemplateView):
    # The HTML template we're going to use, found in the /templates directory
    template_name = "fire_alarm_analysis.html"

    def get_context_data(self, **kwargs):
        # Quick notation to access all complaints
        fire_alarms = FireAlarm.objects.all()

        total_count = fire_alarms.count()
        region_names = ["batemans bay", "bourke", "broken hill", "byron bay", "canberra", \
             "cobar", "cooma", "deniliquin", "dubbo", "grafton", "gunnedah", \
             "katoomba", "kempsey", "kiama", "moree", "newcastle", "sydney", "tamworth", "wagga wagga"]
        regions = {}

        # Iterate over each name in our region_names list
        for reg in region_names:
            # Filter for complaints in each region
            qs = fire_alarms.filter(region=reg)
            # create a data dictionary for the region
            regions[reg] = {}
            regions[reg]['total'] = qs.count()
            regions[reg]['true_alarms'] = qs.filter(true_or_false_alarm=True).count()
            regions[reg]['false_alarms'] = qs.filter(true_or_false_alarm=False).count()
            # get a count of how many complaints total are in the queryset

            # use calculate to find percentages
            regions[reg]['per_true_alarms'] = calculate.percentage(regions[reg]['true_alarms'],regions[reg]['total'])
            regions[reg]['per_false_alarms'] = calculate.percentage(regions[reg]['false_alarms'],regions[reg]['total'])

        return locals()








def drawPiechartSingle(feature_name, data_cube):

    #print "feature_name:", feature_name
    if not FEATURE_TYPE_MAP.has_key(feature_name):
        raise Http404("Features do not exist")

    feature_type = FEATURE_TYPE_MAP[feature_name][0]
    span = ""
    chart_dict = {}
    if feature_type == TYPE_NUMERIC: #numeric type
        span = FEATURE_TYPE_MAP[feature_name][3]
        for i in range( FEATURE_TYPE_MAP[feature_name][1], FEATURE_TYPE_MAP[feature_name][2] + 1, span):
            chart_dict[i] = [0,0]
        #print chart_dict

    for mydict in data_cube:
        feature_val = mydict['features']
        true_cnt = mydict['true_alarm']
        false_cnt = mydict['false_alarm']
        if feature_type == TYPE_NUMERIC:
            feature_val = int(feature_val)
        if not chart_dict.has_key(feature_val):
            chart_dict[feature_val] = [true_cnt, false_cnt]
        else:
            chart_dict[feature_val][0] += true_cnt
            chart_dict[feature_val][1] += false_cnt

    char_list = collections.OrderedDict(sorted(chart_dict.items()))
    xdata = []
    ydata = []
    ydata2 = []
    for key in char_list:
        val = char_list[key]
        xdata.append(key)
        ydata.append(val[0])
        ydata2.append(val[1])

    extra_series = {'tooltip': {'y_start': 'There are ', 'y_end': ' alarms'}}
    chartdata = {
        'x': xdata,
        'name1': 'true alarm', 'y1': ydata, 'extra1': extra_series,
        'name2': 'false alarm', 'y2': ydata2, 'extra2': extra_series
    }
    chartcontainer = 'multibarchart_container'
    charttype = "multiBarChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'color_category': 'category10'
        },
        'height': int(min(1000, len(chart_dict) * 50) *3.5/6),
        'width': int(min(1000, len(chart_dict) * 50)),
    }
    return data



def new_alarm(request):

    result = FireAlarm.objects.filter(instance_no="602172-16062012")
    print len(result)

    if len(result) >= 0:
        result = FireAlarm(instance_no="602172-16062012", alarm_code="465350")
        result.save()
        #print "all data:", FireAlarm.objects.all()

        return render(request, 'new_alarm.html', {"data": "insert successful"})
    else:
        result.delete()
        return render(request, 'new_alarm.html', {"data": "insert failed"})


def predict(request):
    if request.method == "POST":
        a = 'temp' #The backend code
    else:
        form = FireAlarmForm()
    return render(request, "predict.html", {'form' : form})
