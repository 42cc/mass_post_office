from django.contrib.sites.models import Site
from django import template
from django.core.urlresolvers import reverse

from ..utils import encode_data

register = template.Library()


@register.tag
def unsubscribe_link(parser, token):
    try:
        tag_name, obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])
    return UnsubscribeLink(obj)


class UnsubscribeLink(template.Node):

    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def render(self, context):
        user = self.obj.resolve(context)
        data = (user.username, user.email)
        hashed, data = encode_data(data)
        current_site = Site.objects.get_current()
        try:
            url = reverse('mass_post_office:unsubscribe', 
                kwargs={'hashed':hashed, 'data':data})
        except:
            return u'http://%s' % current_site.domain
        # TODO https:// prefix
        return ''.join(['http://', current_site.domain, url])
