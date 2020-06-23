from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader, Context
from django.views.generic import CreateView
from collab.models import competences,client,collaborateurs,outils,experiences, projet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import itemgetter
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import datetime
from xhtml2pdf import pisa 
from bs4 import BeautifulSoup
from docxtpl import DocxTemplate, RichText, Listing
import io
from django.contrib.staticfiles.storage import staticfiles_storage
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
            expesATest = experiences.objects.filter(projetDeLaMission=projetaTest[0].pk)
            if not expesATest:
                statut = "PAS ACTIF"
            else:
                for elt in expesATest:
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
#Liste consultant recherche
def recherche_consultant(request):
    #chargement du template HTML
    template = loader.get_template('collab/liste_consultant_recherche.html')
    #Recherche
    keywords=''
    if request.method=='POST': # soumission du form
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
    mission_du_collab = experiences.objects.filter(collaborateurMission=collaborateurs_id).order_by('-dateDebut')
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
    client_list= client.objects.all().order_by('nomClient')
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
    compe_list= competences.objects.all().order_by('famille')
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
    outils_list= outils.objects.all().order_by('famille')
    page = request.GET.get('page', 1)
    paginator = Paginator(outils_list, 100)
    try:
        tools= paginator.page(page)
    except PageNotAnInteger:
        tools = paginator.page(1)
    except EmptyPage:
        tools = paginator.page(paginator.num_pages)
    context={'tools':tools}
    return HttpResponse(template.render(context, request))

def liste_outil_propre(request):
    template = loader.get_template('collab/liste_outil2.html')
    outils_list= outils.objects.all().order_by('famille')
    context={'tools':outils_list}
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


#Page CV
def page_cv_html(request, collaborateurs_id):
    collab = get_object_or_404(collaborateurs, pk=collaborateurs_id)
    mission_du_collab = experiences.objects.filter(collaborateurMission=collaborateurs_id).order_by('-dateDebut')
    template = loader.get_template('collab/CV_TEST.html')
    context={'collab':collab, 'mission_du_collab':mission_du_collab}
    return HttpResponse(template.render(context, request))

#Page CV en pdf
def page_cv_pdf(request, collaborateurs_id):
    collab = get_object_or_404(collaborateurs, pk=collaborateurs_id)
    mission_du_collab = experiences.objects.filter(collaborateurMission=collaborateurs_id).order_by('-dateDebut')
    template = loader.get_template('collab/CV_TEST.html')
    context={'collab':collab, 'mission_du_collab':mission_du_collab}
    html = template.render(context, request)
    file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')

# Fonction de parsing du HTML pour la generation de CV
def decoupe_html (raw_html):
    soup=BeautifulSoup(raw_html,"html.parser")
    arbre=[]
    #decoupe en grand bloc HTML
    for elt in soup:
        arbre.append(elt)

    #On parcours chaque elt pour le transformer en truc compréhensible par Word dans une liste
    for elt in arbre:
        #recup du tag de début du "chunk"
        tag=elt.name
        #traitement des paragraphe de texte
        if tag == "p":
            texte=elt.text
            place=arbre.index(elt)
            arbre[place]=texte
        #traitement des listes
        elif tag == "ul":
            list_elt=[]
            enfants = elt.findChildren()
            #on récupère tous les elt de la liste
            for chld in enfants:
                list_elt.append(chld.text)
            place=arbre.index(elt)
            arbre[place]=("list",list_elt)
    return(arbre)
def generate_rich_texte (raw_html):
    rich_texte=RichText()
    html_decoupe=decoupe_html(raw_html)
    for elt in html_decoupe:
        print(elt)
        if type(elt)==tuple:
            liste=elt[1]
            string_propre_de_liste=""
            for truc in liste:
                string_propre_de_liste = "• "+string_propre_de_liste+truc+"\n"
            if html_decoupe.index(elt) == 0:
                text=string_propre_de_liste
            else:
                text='\a'+string_propre_de_liste
            rich_texte.add(text)
        else:
            if html_decoupe.index(elt) == 0:
                text=str(elt)
            else:
                text='\a'+str(elt)
            rich_texte.add(text)
    return(rich_texte)
#Page CV docx
def page_cv_word(request, collaborateurs_id):
    collab = get_object_or_404(collaborateurs, pk=collaborateurs_id)
    mission_du_collab = experiences.objects.filter(collaborateurMission=collaborateurs_id).order_by('-dateDebut')
    fichier_template = staticfiles_storage.path('collab/CV_TEST.docx')
    doc = DocxTemplate(fichier_template)
    context = {}
    today = datetime.date.today()
    nom = collab.nomCollaborateur
    prenom = collab.prenomCollaborateur
    nom_sortie = nom + "-"+prenom+"-"+str(today)+".docx"
    titre = collab.titreCollaborateur
    texte_introductif = generate_rich_texte(collab.texteIntroductifCv)
    competencesDuCollab = collab.listeCompetencesCles.all()
    competences=[]
    for compe in competencesDuCollab:
        competences.append(compe.nomCompetence)
    context["nom"]=nom
    context["prenom"]=prenom
    context["titre"]=titre
    context["text_intro"]=texte_introductif
    context["competences"]=competences
    #Il faut encore brancher la fonction propre du dessus
    html_decoupe=['blablablabla',('list','1,2,3'),'reblabla']
    parcours = RichText()
    for elt in html_decoupe:
        if type(elt)==tuple:
            liste=elt[1]
            string_propre_de_liste=""
            for elt in liste:
                string_propre_de_liste = string_propre_de_liste+elt+"\n"
            listing_word=Listing(string_propre_de_liste)
        else:
            text='\n'+str(elt)
            parcours.add(text)
    context["parcours"]=parcours
    trigramme = RichText('blablablablabla un paragraphe t\'a vu \a• poney\n• test\n\t• deuxieme niveau', style='bullet')
    context["trigramme"]=trigramme
    doc.render(context)
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    response = HttpResponse(doc_io.read())
    response["Content-Disposition"] = "attachment; filename="+nom_sortie
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return response