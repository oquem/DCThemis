from django import template
from collab.models import outils, collaborateurs, competences, client, experiences, projet
import datetime
from django.shortcuts import get_object_or_404
import datetime
register = template.Library()

#Definir statut consultant
@register.filter(name='statut_consultant')
def statut_consultant(id_collab):
    test = collaborateurs.objects.filter(pk=id_collab).values("estEnIntercontrat")
    if test[0]['estEnIntercontrat'] == True:
        return "Oui"
    else:
        return "Non"

#recup contexte projet d'une mission ON GARDE ON SAIT JAMAIS
#@register.filter(name='contexte_projet')
#def contexte_projet(id_mission):
#    mission = get_object_or_404(experiences, pk=id_mission)
#    projet_de_la_mission = mission.projetDeLaMission
#    contexte_mission = projet_de_la_mission.contexteMission
#    return contexte_mission

#recup livrables projet d'une mission
@register.filter(name='livrable_projet')
def livrable_projet(id_mission):
    mission = get_object_or_404(experiences, pk=id_mission)
    try:
        projet_de_la_mission = mission.projetDeLaMission
        contexte_mission = projet_de_la_mission.livrables
    except:
        contexte_mission="PAS DE PROJET DEFINI"
    return contexte_mission

#recup benef projet d'une mission
@register.filter(name='benef_projet')
def benef_projet(id_mission):
    mission = get_object_or_404(experiences, pk=id_mission)
    try:
        projet_de_la_mission = mission.projetDeLaMission
        contexte_mission = projet_de_la_mission.benefClient
    except:
        contexte_mission = "PAS DE PROJET DEFINI"
    return contexte_mission

#recup client d'une mission DEVENU USELESS MAIS ON SAIT JAMAIS ON GARDE
#@register.filter(name='recup_client_mission')
#def recup_client_mission(id_mission):
#    expe = get_object_or_404(experiences, pk=id_mission)
#    id_projet_de_la_mission = expe.projetDeLaMission.pk
#    projetaTest = get_object_or_404(projet, pk=id_projet_de_la_mission)
#    client = projetaTest.client
#    return client

#recup Secteur d'un client d'une mission
@register.filter(name='recup_client_secteur')
def recup_client_secteur(id_mission):
    mission = get_object_or_404(experiences, pk=id_mission)
    client_pk = mission.client.pk
    secteur = get_object_or_404(client, pk=client_pk).get_domaineClient_display()
    return secteur

#recup secteur affichage propre d'un client
@register.filter(name='recup_client_secteur_propre')
def recup_client_secteur_propre(client_id):
    secteur = get_object_or_404(client, pk=client_id).get_domaineClient_display()
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
    missions = experiences.objects.filter(client=id_client).count()
    return missions

#Calcul du nombre de missions en cours par client
@register.filter(name='recup_mission_en_cours')
def recup_mission_en_cours(id_client):
    missions = experiences.objects.filter(client=id_client)
    nb=0
    if not missions:
        nb=0
    else:
        for mission in missions:
            date_fin=mission.dateFin
            if date_fin == None:
                nb+=1
            elif date_fin > datetime.date.today():
                nb+=1
            else:
                continue
    return nb

#Definir statut client
@register.filter(name='statut_client')
def statut_client(id_client):
    missions = experiences.objects.filter(client=id_client)
    if not missions:
        statut = "Inactif"
    else:
        for mission in missions:
            date_fin=mission.dateFin
            if date_fin == None:
                statut = "Actif"
                break
            elif date_fin > datetime.date.today():
                statut = "Actif"
                break
            else:
                statut = "Inactif"
    return statut       

#Ajouter deux string
@register.filter
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)