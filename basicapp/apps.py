from django.apps import AppConfig
import pandas as pd

class BasicappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basicapp'


    def ready(self):
        field_info_df = pd.read_csv('./basicapp/django_field.csv')
        # description, fieldtype, option
        field_infos = field_info_df.to_dict('records')
        BasicappConfig.FIELD_INFO = field_infos

