from django import template
from django.conf import settings
from django.template.utils import get_app_template_dirs

register = template.Library()


@register.tag
def sass(parser, token):
    nodelist = parser.parse(('endsass', ))
    parser.delete_first_token()
    return SASSNode(nodelist)


class SASSNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        import sass as libsass
        return libsass.compile(
            string=self.nodelist.render(context),
            output_style=getattr(settings, 'DEBUG', False) and 'compressed' or 'nested',
            include_paths=[str(path) for path in get_app_template_dirs('sass')]
        )
