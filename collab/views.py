from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views.generic import CreateView
from collab.models import competences,client,collaborateurs,outils,experiences, projet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import itemgetter
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import datetime
# Homepage
def index(request):
    template = loader.get_template('collab/index2.html')
    nbConsultant = collaborateurs.objects.count()
    nbConsultantInterco = collaborateurs.objects.filter(estEnIntercontrat=True).count()
    nbConsultantEnMission = nbConsultant - nbConsultantInterco
    txInterco = round((nbConsultantInterco / nbConsultant)*100,2)
    nbCompe = competences.objects.count()
    nbOutils = outils.objects.count()
    nbClient = client.objects.count()
    #Verification qu'un projet est actif (donc avec au moins une mission en cours)
    def verifProjetActif(idProjet):
        projetaTest = projet.objects.filter(pk=idProjet)
        if not projetaTest:
            statut = "PAS ACTIF"
        else:
            expeATest = projetaTest[0].experiencesLiees.all()
            for elt in expeATest:
                dateDeFin = elt.dateFin
                if dateDeFin == None:
                    statut = "ACTIF"
                    break
                elif dateDeFin > datetime.date.today(): 
                    statut = "ACTIF"
                    break
                else:
                    statut = "PAS ACTIF"
        return statut
    #calcul du nombre de client actif (a savoir les clients avec une mission en cours a date) A REWORK car expe n'ont plus de client
    def getClientActif():
        client_total=client.objects.all()
        count=0
        for elt in client_total:
            projets = projet.objects.filter(client=elt.id)
            for elt in projets:
                idProjet = elt.pk
                statut= verifProjetActif(idProjet)
                if statut == "ACTIF":
                    count+=1
                    break
                else:
                    continue
        return(count)
    nbClientActif = getClientActif()
    nbClientInactif = nbClient - nbClientActif
    txClientInactif = round((nbClientInactif / nbClient)*100,2)
    #calcul du nombre de competence moyen par consultant
    def getMoyenneCompetence():
        listeCompe=[]
        listeCollab=collaborateurs.objects.all()
        for elt in listeCollab:
            nb_compe_calcul = elt.listeCompetencesCles.count()
            listeCompe.append(nb_compe_calcul)
        moyenne=(sum(listeCompe)/len(listeCompe))
        return(moyenne)
    def getMoyenneOutil():
        listeOutil=[]
        listeCollab=collaborateurs.objects.all()
        for elt in listeCollab:
            nb_outil_calcul = elt.outilsCollaborateur.count()
            listeOutil.append(nb_outil_calcul)
        moyenne=(sum(listeOutil)/len(listeOutil))
        return(moyenne)
    moyenneOutil = getMoyenneOutil()
    moyenneCompetence = getMoyenneCompetence()
    #calcul top 5 des outils - la fonction retourne l'outil en position N du top
    def getTop5Outils():
        listeCollab=collaborateurs.objects.all()
        dicoOutil_temp={}
        #on récupère les outils de chaque collab et on fait un dictionnaire sous la forme {"outil1":"nb de consultant l'ayant)"}
        for collab in listeCollab:
            liste_outil_collab = collab.outilsCollaborateur.values()
            for elt in liste_outil_collab:
                outil = elt['nomOutil']
                if outil in dicoOutil_temp:
                    nb_temp = dicoOutil_temp.get(outil)
                    dicoOutil_temp[outil]=nb_temp+1
                else:
                    dicoOutil_temp[outil]=1
        #on trie le dictionnaire par valeur
        dicoOutil = sorted(dicoOutil_temp.items(), key=lambda x: x[1], reverse=True)
        #on récupère les valeurs en iterant sur le nouveau dictionnaire et on met dans une liste
        topOutil=[x[0] for x in dicoOutil]
        topfinal=topOutil[:5]
        return topfinal
    topOutilfront = getTop5Outils()    

    #calcul top 5 des competences - la fonction retourne la competence en position N du top
    def getTop5Competences():
        listeCollab=collaborateurs.objects.all()
        dicoCompetences_temp={}
        #on récupère les competences de chaque collab et on fait un dictionnaire sous la forme {"competence1":"nb de consultant l'ayant)"}
        for collab in listeCollab:
            liste_compe_collab = collab.listeCompetencesCles.values()
            for elt in liste_compe_collab:
                competence = elt['nomCompetence']
                if competence in dicoCompetences_temp:
                    nb_temp = dicoCompetences_temp.get(competence)
                    dicoCompetences_temp[competence]=nb_temp+1
                else:
                    dicoCompetences_temp[competence]=1
        #on trie le dictionnaire par valeur
        dicoCompetences = sorted(dicoCompetences_temp.items(), key=lambda x: x[1], reverse=True)
        #on récupère les valeurs en iterant sur le nouveau dictionnaire et on met dans une liste
        topCompetence=[x[0] for x in dicoCompetences]
        topfinal=topCompetence[:5]
        return topfinal
    topCompetencefront = getTop5Competences()   
    context={
    "nbConsultant":nbConsultant,
    "nbConsultantInterco":nbConsultantInterco,
    "txInterco":txInterco,
    "nbConsultantEnMission":nbConsultantEnMission,
    "nbClient":nbClient,
    "nbClientActif":nbClientActif,
    "nbClientInactif":nbClientInactif,
    "txClientInactif":txClientInactif,
    "nbCompe":nbCompe,
    "moyenneCompetence":moyenneCompetence,
    'topCompetencefront':topCompetencefront,
    'nbOutils':nbOutils,
    'moyenneOutil':moyenneOutil,
    'topOutilfront':topOutilfront
    }
    return HttpResponse(template.render(context, request))

# Liste consultant PAGINEE
def liste_consultant(request):
    template = loader.get_template('collab/liste_consultant_recherche.html')
    collab_list= collaborateurs.objects.all().order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(collab_list, 10)
    try:
        collabs= paginator.page(page)
    except PageNotAnInteger:
        collabs = paginator.page(1)
    except EmptyPage:
        collabs = paginator.page(paginator.num_pages)
    context={'collabs':collabs}
    return HttpResponse(template.render(context, request))
#Liste consultant recherche WORK IN PROGRESS
def recherche_consultant(request):
    #chargement du template HTML
    template = loader.get_template('collab/liste_consultant_recherche.html')
    #Recherche
    keywords=''
    if request.method=='POST': # form was submitted
        keywords = request.POST.get("nom", "") # <input type="text" name="nom">
        all_queries = None
        search_fields = ('nomCollaborateur','prenomCollaborateur')
        for keyword in keywords.split(' '):
            keyword_query = None
            for field in search_fields:
                each_query = Q(**{field + '__icontains': keyword})
                if not keyword_query:
                    keyword_query = each_query
                else:
                    keyword_query = keyword_query | each_query
                    if not all_queries:
                        all_queries = keyword_query
                    else:
                        all_queries = all_queries & keyword_query

        collab_list = collaborateurs.objects.filter(all_queries).distinct()
        page = request.GET.get('page', 1)
        paginator = Paginator(collab_list, 5)
        try:
            collabs= paginator.page(page)
        except PageNotAnInteger:
            collabs = paginator.page(1)
        except EmptyPage:
            collabs = paginator.page(paginator.num_pages)
        context={'collabs':collabs}
        return HttpResponse(template.render(context, request))

    else: # no data submitted
        collab_list= collaborateurs.objects.all().order_by('nomCollaborateur')
        page = request.GET.get('page', 1)
        paginator = Paginator(collab_list, 10)
        try:
            collabs= paginator.page(page)
        except PageNotAnInteger:
            collabs = paginator.page(1)
        except EmptyPage:
            collabs = paginator.page(paginator.num_pages)
        context={'collabs':collabs}
        return HttpResponse(template.render(context, request))

#Detail consultant
def collaborateur_detail(request, collaborateurs_id):
    collab = get_object_or_404(collaborateurs, pk=collaborateurs_id)
    mission_du_collab = experiences.objects.filter(collaborateurMission=collaborateurs_id)
    template = loader.get_template('collab/detail_consultant2.html')
    context={'collab':collab, 'mission_du_collab':mission_du_collab}
    return HttpResponse(template.render(context, request))
#Ajout d'un consultant
class collaborateursCreateView(CreateView):
    model = collaborateurs
    fields = ('nomCollaborateur', 'prenomCollaborateur','titreCollaborateur','texteIntroductifCv','nbAnneeExperience','listeCompetencesCles','formation','parcours','methodologie','langues','outilsCollaborateur','estEnIntercontrat')
    success_url = 'succes/'
def reussite_ajout_collaborateurs(request):
    template = loader.get_template('collab/reussite_ajout_collaborateurs2.html')
    context={}
    return HttpResponse(template.render(context, request))

#Liste client PAGINEE
def liste_client(request):
    template = loader.get_template('collab/liste_client2.html')
    client_list= client.objects.all().order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(client_list, 10)
    try:
        clients= paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)
    context={'clients':clients}
    return HttpResponse(template.render(context, request))
#Ajout d'un client
class clientCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = client
    fields = ('nomClient', 'domaineClient','logoClient')
    success_url = 'succes/'
def reussite_ajout_client(request):
    template = loader.get_template('collab/reussite_ajout_client2.html')
    context={}
    return HttpResponse(template.render(context, request))    
#Liste compétences PAGINEE
def liste_competence(request):
    template = loader.get_template('collab/liste_competence2.html')
    compe_list= competences.objects.all().order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(compe_list, 10)
    try:
        compes= paginator.page(page)
    except PageNotAnInteger:
        compes = paginator.page(1)
    except EmptyPage:
        compes = paginator.page(paginator.num_pages)
    context={'compes':compes}
    return HttpResponse(template.render(context, request))
#Ajout d'une competence
class competencesCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = competences
    fields = ('nomCompetence', 'famille')
    success_url = 'succes/'

def reussite_ajout_competence(request):
    template = loader.get_template('collab/reussite_ajout_compe2.html')
    context={}
    return HttpResponse(template.render(context, request))

#Liste outil REELLEMENT PAGINEE
def liste_outil(request):
    template = loader.get_template('collab/liste_outil2.html')
    outils_list= outils.objects.all().order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(outils_list, 10)
    try:
        tools= paginator.page(page)
    except PageNotAnInteger:
        tools = paginator.page(1)
    except EmptyPage:
        tools = paginator.page(paginator.num_pages)
    context={'tools':tools}
    return HttpResponse(template.render(context, request))

class outilsCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = outils
    fields = ('nomOutil', 'famille')
    success_url = 'succes/'
def reussite_ajout_outil(request):
    template = loader.get_template('collab/reussite_ajout_outil2.html')
    context={}
    return HttpResponse(template.render(context, request))