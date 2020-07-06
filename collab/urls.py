from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultant/', views.liste_consultant, name='liste_consultant'),
    path('consultant/<int:collaborateurs_id>/', views.collaborateur_detail, name='collaborateur_detail'),
    path('consultant/<int:collaborateurs_id>/cv_html', views.page_cv_html, name='page_cv_html'),
    path('consultant/<int:collaborateurs_id>/cv_html/pdf', views.page_cv_pdf, name='page_cv_pdf'),
    path('consultant/<int:collaborateurs_id>/cv_word', views.page_cv_word, name='page_cv_word'),
    path('consultant/ajout/', views.collaborateursCreateView.as_view(), name='collaborateursCreateView'),
    path('consultant/ajout/succes/', views.reussite_ajout_collaborateurs, name='reussite_ajout_collaborateurs'),
    path('client/', views.liste_client, name='liste_client'),
    path('client/ajout/', views.clientCreateView.as_view(), name='clientCreateView'),
    path('client/ajout/succes/', views.reussite_ajout_client, name='reussite_ajout_client'),
    path('competence/', views.liste_competence, name='liste_competence'),
    path('competence/ajout/', views.competencesCreateView.as_view(), name='competencesCreateView'),
    path('competence/ajout/succes/', views.reussite_ajout_competence, name='reussite_ajout_competence'),
    path('outil/', views.liste_outil_propre, name='liste_outil_propre'),
    path('outil/ajout/', views.outilsCreateView.as_view(), name='outilsCreateView'),
    path('outil/ajout/succes/', views.reussite_ajout_outil, name='reussite_ajout_outil'),
    path('intervention/', views.liste_intervention, name='liste_intervention'),
]