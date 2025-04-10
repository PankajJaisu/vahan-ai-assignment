from django.urls import path
from core.views import (
    UploadPaperView,
    SearchAndClassifyView,
    ProcessDOIView,
    ProcessAcademicRepoURLView,
    ResearchPaperListView,
    ResearchPaperDetailView,
    SynthesizeSummaryView
)

urlpatterns = [
    path('upload/', UploadPaperView.as_view(), name="upload-paper"),
    path('search/', SearchAndClassifyView.as_view(), name="search-classify"),  # GET
    path('process-url/', SearchAndClassifyView.as_view(), name="process-url"),  # POST
    path('process-doi/', ProcessDOIView.as_view(), name="process-doi"),
    path('process-academic-url/', ProcessAcademicRepoURLView.as_view(), name="process-academic-url"),
    path('papers/', ResearchPaperListView.as_view(), name="list-papers"),
    path('papers/<int:pk>/', ResearchPaperDetailView.as_view(), name="paper-detail"),
    path('synthesize/', SynthesizeSummaryView.as_view(), name="synthesize-summary"),
]
