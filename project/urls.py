from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.static import serve as static_serve
from django.views.generic import TemplateView
from building_and_safety.views import *
from building_and_safety import views
from django.contrib.admin.views.decorators import staff_member_required
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # This is the URL Varnish will ping to check the server health.
    url(r'^app_status/$', 'toolbox.views.app_status', name='status'),

    url(r'^features/$', views.get_features, name='get_features'),
    #url(r'^data_cubes/(?P<feature_file_name>[\w\-\_]+)', views.get_data_cubes, name='get_data_cubes'),
    url(r'^data_cubes/(?P<feature_file_name>[\w\-\_]+)', views.get_data_cubes2, name='get_data_cubes'),
    #url(r'^complaint/(?P<csr>[0-9]{6})/$', ComplaintDetail.as_view(), name="complaint_detail"),
    url(r'^fire_alarm_analysis/$', FireAlarmAnalysis.as_view(), name='fire_alarm_analysis'),
    #url(r'^complaint_type_breakdown/$', ComplaintTypeBreakdown.as_view(), name='complaint_type_breakdown'),
    #url(r'^api/complaints.json$', open_complaints_json, name='complaints-json'),
    #url(r'^api/closed_complaints.json$', closed_complaints_json, name='closed-complaints-json'),
    #url(r'^complaints-map/$', ComplaintsMap.as_view(), name='complaints-map'),

    #url(r'^piechart/(?P<attr_name>[\w]+)/$', views.piechart, name='piechart'),

    url(r'^new_alarm/$', views.new_alarm, name='new_alarm'),

    url(r'^predict/$', views.predict, name='predict'),

)


if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        url(r'^static/(?P<path>.*)$', 'serve', {
            'document_root': settings.STATIC_ROOT,
            'show_indexes': True,
        }),
        url(r'^media/(?P<path>.*)$', 'serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True,
        }),
    )

if settings.PRODUCTION:
    urlpatterns += patterns('',
        url(r'^munin/(?P<path>.*)$', staff_member_required(static_serve), {
            'document_root': settings.MUNIN_ROOT,
        })
   )
