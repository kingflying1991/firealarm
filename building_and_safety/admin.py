from django.contrib import admin
from building_and_safety.models import *

# Register your models here.
class FireAlarmAdmin(admin.ModelAdmin):
    list_display = ('instance_number','creation_date','activation_date','year', 'month', 'alarm_code','incd_address',
        'np_id','alarm_type','incident_type','call_source','repeat_count', "x", "y", "region")
    list_filter = ['year', 'month','alarm_type','incident_type','call_source']
    search_fields = ['instance_number']
    fieldsets = (
        (('Raw data fields'),
            {'fields': ('instance_number',
                            ('alarm_code', 'alarm_type', 'incident_type', 'repeat_count'),
                            ('region', 'x', 'y', 'incd_address'),
                            ('creation_date', 'activation_date', 'year', 'month', )
                            )
            }
        ),
    )

admin.site.register(FireAlarm, FireAlarmAdmin)
admin.site.register(Features)
