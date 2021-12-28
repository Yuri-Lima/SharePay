from django.urls import path, include
from landpage.views import (
    IndexLandPage,
)

app_name = 'landpage'

urlpatterns = [
    # index
    path('', IndexLandPage.as_view(), name='getstarted')
]
