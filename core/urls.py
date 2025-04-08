from django.urls import path
from core.views import UploadPaperView,SearchAndClassifyView,SearchAndClassifyView,ProcessDOIView

urlpatterns = [
    path('upload/', UploadPaperView.as_view()),
    path('search/', SearchAndClassifyView.as_view()),
    path('process-url/', SearchAndClassifyView.as_view()),
    path('process-doi/', ProcessDOIView.as_view()),
]