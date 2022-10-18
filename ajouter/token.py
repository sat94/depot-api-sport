from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import AbstractBaseUser
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: AbstractBaseUser, timestamp):
        return (
            six.text_type(user.pk)+ six.text_type(timestamp) + six.text_type(user.is_active)           
        )
account_activation_token= AccountActivationTokenGenerator()