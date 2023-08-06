import requests

from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.backends.django import DjangoTemplates
from django.template.engine import Engine

class TemplateFetchError(Exception):
    pass

class DjazztroBackend(DjangoTemplates):

    app_dirname = ""
        
    def get_template(self, template_name):
        try:
            resp = requests.get(f"http://localhost:3000/{template_name}.html")
            if resp.status_code == 404:
                raise TemplateFetchError(f"Couldn't find template: {template_name}")
            template_text = resp.text.replace("src=\"/", "src=\"http://localhost:3000/")
            return self.from_string(template_text)
        except requests.ConnectionError:
            raise TemplateFetchError(f"Can't connect to Astro, is it running? (Tried: http://localhost:3000)")
    
    
class Template:

    def __init__(self, template):
        self.template = template

    def render(self, context=None, request=None):
        if context is None:
            context = {}
        if request is not None:
            context['request'] = request
            context['csrf_input'] = csrf_input_lazy(request)
            context['csrf_token'] = csrf_token_lazy(request)
        return self.template.render(context)

