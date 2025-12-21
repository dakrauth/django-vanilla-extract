from django.views.generic import RedirectView, View

from vanilla_extract.model_views import (CreateView, DeleteView, DetailView,
                                         GenericModelView, ListView,
                                         UpdateView)
from vanilla_extract.views import FormView, GenericView, TemplateView

__version__ = "4.0.0"
__all__ = (
    "View",
    "GenericView",
    "GenericModelView",
    "RedirectView",
    "TemplateView",
    "FormView",
    "ListView",
    "DetailView",
    "CreateView",
    "UpdateView",
    "DeleteView",
)
