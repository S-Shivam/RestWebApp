from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = DefaultRouter()
router.register('visit', views.VisitViewsetModel, basename='visit')

app_name = 'visit'
urlpatterns = [

    # visit/viewsetapi/
    path('viewsetapi/', include(router.urls)),
    # visit/viewsetapi/<int:pk>/
    # path('viewsetapi/<int:pk>/', include(router.urls)),

    # visit/
    path('', views.index, name='index'),
    # visit/showlist/
    path('showlist/', views.VisitDataFilter.as_view(), name='showlist'),
    # visit/showlist/<uid>/
    path('showlist/<int:uid>/', views.VisitDataDetail.as_view(), name='showlistid'),
    # visit/generic/showlist/
    path('generic/showlist/', views.GenericListAndDetails.as_view(), name='generic_list'),
    # visit/generic/showlist/<id>/
    path('generic/showlist/<int:id>/', views.GenericListAndDetails.as_view(), name='generic_detail'),
    # visit/impdata
    path('impdata', views.importdata, name='importdata'),
]


