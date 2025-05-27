from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio'

    # Override the ready method to import signals
    def ready(self):
        import portfolio.signals
