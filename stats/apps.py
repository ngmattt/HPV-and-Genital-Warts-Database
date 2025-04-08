from django.apps import AppConfig


class StatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'

class Meta:
    managed = False  # Because we already created the tables
    db_table = 'WartsStats'  # e.g., 'WartsStats'
