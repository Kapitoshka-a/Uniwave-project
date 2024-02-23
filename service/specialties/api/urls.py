from django.urls import path
from .views import *

urlpatterns = [
    path('specialties/', SpecialtiesList.as_view(), name='specialty-list'),
    path('specialties/<slug:slug>/', SpecialtyDetail.as_view(), name='specialty-detail'),
    path('specialties/<slug:slug>/comments/', CommentListCreate.as_view(), name='comment-list'),
    path('specialties/<slug:slug>/comments/<int:pk>', CommentDetail.as_view(), name='comment-detail'),
    path('universities/', UniversityList.as_view(), name='university-list'),
    path('universities/<int:pk>/', UniversityDetail.as_view(), name='university-detail'),
]
