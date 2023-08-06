from django.conf import settings
from django.contrib.sites.models import Site
from templated_mail.mail import BaseEmailMessage

from .shortcuts import get_current_site

class EmailSendMixin:
    @property
    def origin_site(self):
        if not self.request:
            raise Site.DoesNotExist
        return get_current_site(self.request)
        
    def send(self, to, *args, **kwargs):
        self.render()

        current_site = self.origin_site

        from_email = '"{email_sender}" <{email_address}>'.format(
            email_sender=current_site.name,
            email_address='notifications@noundb.com'.format(
                domain=current_site.domain
            ),
        )

        self.to = to
        self.cc = kwargs.pop('cc', [])
        self.bcc = kwargs.pop('bcc', [])
        self.reply_to = kwargs.pop('reply_to', [])
        self.from_email = from_email

        super(BaseEmailMessage, self).send(*args, **kwargs)

    def get_base_context_data(self, **kwargs):
        ctx = super(BaseEmailMessage, self).get_context_data(**kwargs)
        context = dict(ctx, **self.context)

        pwa_domain = ''
        if self.request:
            pwa_domain = self.request.META.get('HTTP_ORIGIN')
            if 'user' not in context:
                context['user'] = self.request.user

        context.update({
            'protocol': 'https',
            'site': self.origin_site,
            'pwa_domain': pwa_domain,
        })

        return context
