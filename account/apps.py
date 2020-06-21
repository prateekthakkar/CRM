from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'

    # overwite method for signals
    def ready(self):
        import account.signals
