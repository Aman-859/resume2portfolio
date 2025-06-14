
from django.urls import path
from django.conf import settings
from .views import * 
from django.conf.urls.static import static

urlpatterns = [
     path('', image_to_text, name='image_to_text'),
      path('Modern_Minimal/', Modern_Minimal, name='modern_minimal'),
      path('Creative_Bold/', Creative_Bold , name='Creative_Bold'),
      path('Tech_Professional/',Tech_Professional, name='Tech_Professional'),
      path('Portfolio_Grid/', Portfolio_Grid ,name='Portfolio_Grid'),
      path('resume/<uuid:resume_id>/', portfolio_view, name='portfolio_view'),
      path('save_and_share/', save_and_share, name='save_and_share'),
]

 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
