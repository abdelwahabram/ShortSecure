from .models import Url
from django.forms import ModelForm

class UrlForm(ModelForm):
    class Meta():
        model = Url
        fields = ['url']