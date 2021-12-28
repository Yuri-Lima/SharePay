
from django.views.generic import (
    TemplateView,
    FormView,
)

# Create your views here.
class IndexLandPage(TemplateView):
    template_name = 'landpage/index.html'

    # def get_context_data(self, **kwargs):
        
    #     return super(IndexLandPage, self).get_context_data(**kwargs)