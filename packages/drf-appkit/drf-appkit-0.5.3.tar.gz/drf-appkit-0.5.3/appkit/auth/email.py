from django.contrib.auth.tokens import default_token_generator

from djoser import utils as djoser_utils
from djoser.conf import settings as djoser_settings
from djoser.email import (
    ActivationEmail as BaseActivationEmail,
    PasswordResetEmail as BasePasswordResetEmail,
)

from ..email import EmailSendMixin


class ActivationEmail(EmailSendMixin, BaseActivationEmail):
    def get_context_data(self, **kwargs):
        context = self.get_base_context_data(**kwargs)

        user = context.get('user')
        context['uid'] = djoser_utils.encode_uid(user.pk)
        context['token'] = default_token_generator.make_token(user)
        context['url'] = djoser_settings.ACTIVATION_URL.format(**context)

        return context


class PasswordResetEmail(EmailSendMixin, BasePasswordResetEmail):
    def get_context_data(self, **kwargs):
        context = self.get_base_context_data(**kwargs)

        user = context.get('user')
        context.update({
            'uid': djoser_utils.encode_uid(user.pk),
            'token': default_token_generator.make_token(user),
        })
        context['url'] = djoser_settings.PASSWORD_RESET_CONFIRM_URL.format(**context)

        return context
