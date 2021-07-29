from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class Index(TemplateView):
    template_name = 'webapp/index.html'


class ForCreators(TemplateView):
    template_name = 'webapp/for_creators.html'


class ForOrganizations(TemplateView):
    template_name = 'webapp/for_organizations.html'