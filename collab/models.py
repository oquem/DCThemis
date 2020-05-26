from django.db import models
from django.forms import ModelForm
from django.conf import settings

#Clients
class domaine(models.Model):
    nomDomaine = models.CharField(max_length=300)
    def __str__(self):
        return self.nomDomaine
    class Meta: 
        verbose_name = 'Secteur Client'

class client(models.Model):
    nomClient = models.CharField(max_length=250)
    domaineClient = models.ForeignKey(domaine, on_delete=models.CASCADE)
    logoClient = models.ImageField(upload_to='collab/static/collab', blank=True, null=True)
    def __str__(self):
        return self.nomClient

#Outils 
class familleOutils(models.Model):
    nomFamilleOutils = models.CharField(max_length=250)
    def __str__(self):
        return self.nomFamilleOutils

class outils(models.Model):
    nomOutil = models.CharField(max_length=250)
    famille = models.ForeignKey(familleOutils, on_delete=models.CASCADE)
    def __str__(self):
        return self.nomOutil

#Compétences
class familleCompetences(models.Model):
    nomFamilleCompetence = models.CharField(max_length=250)
    def __str__(self):
        return self.nomFamilleCompetence

class competences(models.Model):
    nomCompetence = models.CharField(max_length=250)
    famille = models.ForeignKey(familleCompetences, on_delete=models.CASCADE)
    def __str__(self):
        return self.nomCompetence



#Collaborateur
class collaborateurs(models.Model):
    nomCollaborateur = models.CharField(max_length=200)
    prenomCollaborateur = models.CharField(max_length=200)
    titreCollaborateur = models.CharField(max_length=200)
    texteIntroductifCv = models.TextField(default='')
    nbAnneeExperience = models.IntegerField()
    codePostal = models.CharField(default='',max_length=200)
    telephone = models.CharField(default='',max_length=200)
    mail = models.CharField(default='',max_length=200)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    TYPE_CONTRAT = (
        ('I', 'Interne'),
        ('E', 'Externe'),
    )
    typeContrat = models.CharField(max_length=1, choices=TYPE_CONTRAT, default='I')
    tjm=models.DecimalField(decimal_places=2,max_digits=6, default=0.0)
    listeCompetencesCles = models.ManyToManyField(competences)
    formation = models.TextField()
    parcours = models.TextField()
    methodologie = models.TextField()
    langues = models.TextField()
    outilsCollaborateur = models.ManyToManyField(outils)
    estEnIntercontrat = models.BooleanField(default=False)
    def __str__(self):
        return self.nomCollaborateur
    def get_absolute_url(self):
        return "/consultant/%i/" % self.id
    class Meta: 
        verbose_name = 'Consultant'

#Experiences
class experiences(models.Model):
    nomMission = models.CharField(max_length=300)
    niveauIntervention = models.CharField(max_length=300, default="")
    client = models.ForeignKey(client, on_delete=models.CASCADE)
    dateDebut = models.DateField('date de début de mission')
    dateFin = models.DateField('date de fin de mission', blank=True, null=True)
    nbJourHomme = models.IntegerField()
    contexteMission = models.TextField(default='')
    descriptifMission = models.TextField()
    environnementMission =  models.TextField()
    collaborateurMission = models.ForeignKey(collaborateurs, on_delete=models.CASCADE, default='')
    def __str__(self):
        return self.nomMission
    def get_absolute_url(self):
        collab=self.collaborateurMission.id
        return "/consultant/%i/" % collab
    class Meta: 
        verbose_name = 'Intervention'
#BU
class BU(models.Model):
    nomBU = models.CharField(max_length=250)
    def __str__(self):
        return self.nomBU
    class Meta: 
        verbose_name = 'Business Unit'
#Gestion Managériale Projet
class gestionManagerialeProjet(models.Model):
    dateDebut = models.DateField('date de début de la gestion du Projet', null=True)
    dateFin = models.DateField('date de fin de la gestion du Projet', blank=True, null=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return str('%s %s' %(self.dateDebut, self.manager))

#Gestion Commerciale Projet
class gestionCommercialeProjet(models.Model):
    dateDebut = models.DateField('date de début de la gestion commerciale du Projet', null=True)
    dateFin = models.DateField('date de fin de la gestion commerciale du Projet', blank=True, null=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return str('%s %s' %(self.dateDebut, self.manager))

#Projet (un projet peut englober plusieurs Expériences par exemple projet SAPHIR)
class projet(models.Model):
    nomProjet = models.CharField(max_length=300)
    resumeProjet = models.TextField(default='')
    client = models.ForeignKey(client, on_delete=models.CASCADE, null=True)
    budget = models.DecimalField(decimal_places=2,max_digits=11, default=0.0)
    nbJourHomme = models.IntegerField()
    livrables = models.TextField(default='')
    benefClient = models.TextField(default='')
    contexteMission = models.TextField(default='')
    dateDebut = models.DateField('date de début du Projet', null=True)
    dateFin = models.DateField('date de fin du Projet', blank=True, null=True)
    BUProjet = models.ForeignKey(BU, on_delete=models.SET_NULL, null=True)
    gestionManageriale = models.ManyToManyField(gestionManagerialeProjet)
    gestionCommerciale = models.ManyToManyField(gestionCommercialeProjet)
    experiencesLiees = models.ManyToManyField(experiences)
    def __str__(self):
        return self.nomProjet

#Langues
class langue(models.Model):
    nomLangue = models.CharField(max_length=500)
    NIVEAU_LANGUE = (
        ('A0', 'Débutant'),
        ('A1', 'Élémentaire'),
        ('A2','Pré-intermédiaire'),
        ('B1','Intermédiaire'),
        ('B2','Intermédiaire supérieur'),
        ('C1','Avancé'),
        ('C2','Courant'),
    )
    niveauLangue = models.CharField(max_length=2, choices=NIVEAU_LANGUE, default='A0')
    def __str__(self):
        return self.nomProjet


