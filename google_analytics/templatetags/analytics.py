from django import template
from django.conf import settings
from django.template import Context, loader


register = template.Library()


def do_get_analytics(parser, token):
    contents = token.split_contents()
    tag_name = contents[0]
    template_name = 'google_analytics/{}_template.html'.format(tag_name)
    if len(contents) == 2:
        code = contents[1]
    elif len(contents) == 1:
        code = None
    else:
        raise template.TemplateSyntaxError, "%r cannot take more than one argument" % tag_name

    if not (code[0] == code[-1] and code[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    code = code[1:-1]
    current_site = None

    return AnalyticsNode(current_site, code, template_name)


class AnalyticsNode(template.Node):
    def __init__(self, site=None, code=None,
                 template_name='google_analytics/analytics_template.html'):
        self.site = site
        self.code = code
        self.template_name = template_name

    def render(self, context):
        if self.site:
            code_set = self.site.analytics_set.all()
            if code_set:
                code = code_set[0].analytics_code
            else:
                return ''
        elif self.code:
            code = self.code
        else:
            return ''

        if code.strip() != '':
            t = loader.get_template(self.template_name)
            c = Context({
                'analytics_code': code,
                'track_page_load_time': getattr(
                    settings, "GOOGLE_ANALYTICS_TRACK_PAGE_LOAD_TIME", True),
            })
            return t.render(c)
        else:
            return ''

register.tag('analytics', do_get_analytics)
register.tag('analytics_async', do_get_analytics)
