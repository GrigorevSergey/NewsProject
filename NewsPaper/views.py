from django.http import HttpResponse
from django.views import View
from django.utils.translation import gettext as _


class Page(View):
    def get(self, request):
        string = _('Welcome to News')

        return HttpResponse(string)