from django import template
from collab.models import outils, collaborateurs, competences, client, experiences, projet
import datetime
from django.shortcuts import get_object_or_404
register = template.Library()

#Definir statut consultant
@register.filter(name='statut_consultant')
def statut_consultant(id_collab):
    test = collaborateurs.objects.filter(pk=id_collab).values("estEnIntercontrat")
    if test[0]['estEnIntercontrat'] == True:
        return "Oui"
    else:
        return "Non"

#recup contexte projet d'une mission
@register.filter(name='contexte_projet')
def contexte_projet(id_mission):
    projet_de_la_mission = get_object_or_404(projet, experiencesLiees=id_mission)
    contexte_mission = projet_de_la_mission.contexteMission
    return contexte_mission

#recup livrables projet d'une mission
@register.filter(name='livrable_projet')
def livrable_projet(id_mission):
    projet_de_la_mission = get_object_or_404(projet, experiencesLiees=id_mission)
    contexte_mission = projet_de_la_mission.livrables
    return contexte_mission

#recup benef projet d'une mission
@register.filter(name='benef_projet')
def benef_projet(id_mission):
    projet_de_la_mission = get_object_or_404(projet, experiencesLiees=id_mission)
    contexte_mission = projet_de_la_mission.benefClient
    return contexte_mission

#recup client d'une mission
@register.filter(name='recup_client_mission')
def recup_client_mission(id_mission):
    projet_de_la_mission = get_object_or_404(projet, experiencesLiees=id_mission)
    client = projet_de_la_mission.client
    return client

#recup Secteur d'un client d'une mission
@register.filter(name='recup_client_secteur')
def recup_client_secteur(id_mission):
    projet_de_la_mission = get_object_or_404(projet, experiencesLiees=id_mission)
    client = projet_de_la_mission.client
    secteur = client.domaineClient
    return secteur

#Calcul du nombre de consultant par outil
@register.filter(name='nb_consultant_outil')
def nb_consultant_outil(id_outil):
    nb = collaborateurs.objects.filter(outilsCollaborateur=id_outil).count()
    return nb

#Calcul du nombre de consultant par competence
@register.filter(name='nb_consultant_compe')
def nb_consultant_compe(id_compe):
    nb = collaborateurs.objects.filter(listeCompetencesCles=id_compe).count()
    return nb

#Calcul du nombre de missions totales par client
@register.filter(name='recup_mission')
def recup_mission(id_client):
    nb = experiences.objects.filter(client=id_client).count()
    return nb

#Calcul du nombre de missions en cours par client
#@register.filter(name='recup_mission_en_cours')
#def recup_mission_en_cours(id_client):
#    nb = experiences.objects.filter(dateFin__gte=datetime.date.today(),client=id_client).count()
#    nb2 = experiences.objects.filter(dateFin=None,client=id_client).count()
#    nb3=nb+nb2
#    return nb3

#Definir statut client
#@register.filter(name='statut_client')
#def statut_client(id_client):
#    nb = experiences.objects.filter(dateFin__gte=datetime.date.today(),client=id_client).count()
#    nb2 = experiences.objects.filter(dateFin=None,client=id_client).count()
#    if nb > 0:
#        return "Oui"
#    elif nb2 > 0:
#        return "Oui"
#    else:
#        return "Non"

#Ajouter deux string
@register.filter
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)