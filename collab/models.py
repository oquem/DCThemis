from django.db import models
from django.forms import ModelForm
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

def get_display(key, list):
    d = dict(list)
    if key in d:
        return d[key]
    return None
#Clients
class client(models.Model):
    nomClient = models.CharField(max_length=250)
    SECTEUR = (
        ('1','Activités immobilières '),
        ('2','Agriculture'),
        ('3','Agroalimentaire'),
        ('4','Armée, sécurité'),
        ('5','Art, Design'),
        ('6','Assurance'),
        ('7','Audiovisuel, Spectacle, Cinéma'),
        ('8','Audit, Études et conseils, Expertise'),
        ('9','Automobile et  réparation automobile '),
        ('10','Banque'),
        ('11','Bois / Papier / Carton'),
        ('12','BTP, Architecture'),
        ('13','Chimie / Parachimie'),
        ('14','Commerce / Négoce'),
        ('15','Commerce du jeu '),
        ('16','Construction aéronautique, ferroviaire et navale'),
        ('17','Culture, Artisanat d\'art'),
        ('18','Distribution'),
        ('19','Droit, justice'),
        ('20','e-commerce'),
        ('21','Édition / imprimerie / reproduction / Communication / Multimédia'),
        ('22','Edition, Journalisme'),
        ('23','Électricité'),
        ('24','Electronique, Electrotechnique'),
        ('25','Energie'),
        ('26','Enseignement et éducation '),
        ('27','Environnement'),
        ('28','Fonction publique'),
        ('29','Hôtellerie , Café, Tabac et Restauration'),
        ('30','Imprimerie'),
        ('31','Industrie du tabac '),
        ('32','Industrie pharmaceutique'),
        ('33','Informatique, Numérique et Réseaux'),
        ('34','Logistique'),
        ('35','Machines et équipements'),
        ('36','Maintenance, entretien'),
        ('37','Marketing, publicité, Communication'),
        ('38','Matériaux de construction, , Transformations'),
        ('39','Métallurgie'),
        ('40','Mode / Textile / Habillement / Chaussure'),
        ('41','Plastique / Caoutchouc'),
        ('42','Poste et télécommunications '),
        ('43','Recherche et développement '),
        ('44','Récupération '),
        ('45','Santé, médical'),
        ('46','Services aux entreprises'),
        ('47','Social, Services à la personne'),
        ('48','Sport et loisirs'),
        ('49','Tourisme'),
        ('50','Transports')
    )
    domaineClient = models.CharField(max_length=2, choices=SECTEUR, default='1')
    logoClient = models.ImageField(upload_to='collab/static/collab', blank=True, null=True)
    def domaineClient_verbose(self):
        return get_display(self.domaineClient, SECTEUR)  
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

#Gestion Managériale Consultant
class gestionManagerialeConsultant(models.Model):
    dateDebut = models.DateField('date de début de la gestion du consultant', null=True)
    dateFin = models.DateField('date de fin de la gestion du consultant', blank=True, null=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return str('%s %s' %(self.dateDebut, self.manager))

#Table pour Expertise Sectorielle
class expertiseSectorielle(models.Model):
    nom = models.CharField(max_length=500)
    def __str__(self):
        return self.nom

#Formation et Certification
class formation(models.Model):
    diplome = models.CharField(max_length=500)
    ecole = models.CharField(max_length=500)
    def __str__(self):
        return str('%s %s' %(self.diplome, self.ecole))

#Obtention Formation
class obtentionFormation(models.Model):
    dateObtention = models.DateField('date d\'obtention du diplome ou certification', null=True)
    formation = models.ForeignKey(formation, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return str('%s %s' %(self.dateObtention, self.formation))

#Niveaux d'interventions
class niveauIntervention(models.Model):
    libelle = models.CharField(max_length=500)
    def __str__(self):
        return self.libelle
#Langues
class LanguesParlee(models.Model):
    nom = models.CharField(max_length=500)
    NIVEAU_LANGUE = (
        ('Debutant', 'Debutant'),
        ('Courant','Courant'),
        ('Bilingue', 'Bilingue'),
    )
    niveau = models.CharField(max_length=10, choices=NIVEAU_LANGUE, default='Debutant')
    def __str__(self):
        return str('%s %s' %(self.nom, self.niveau))

#Collaborateur
class collaborateurs(models.Model):
    nomCollaborateur = models.CharField(max_length=200)
    prenomCollaborateur = models.CharField(max_length=200)
    titreCollaborateur = models.CharField(max_length=200)
    dateDeNaissance = models.DateField('date de naissance du consultant', blank=True, null=True)
    texteIntroductifCv = models.TextField(default='')
    nbAnneeExperience = models.IntegerField()
    codePostal = models.CharField(default='',max_length=200)
    telephone = models.CharField(default='',max_length=200)
    mail = models.CharField(default='',max_length=200)
    manager = models.ManyToManyField(gestionManagerialeConsultant)
    TYPE_CONTRAT = (
        ('I', 'CDI'),
        ('D', 'CDD'),
        ('N', 'Intérimaire'),
        ('A', 'Contrat d\'alternance'),
        ('X', 'Indépendant'),
        ('S', 'Sous-traitant'),
    )
    typeContrat = models.CharField(max_length=1, choices=TYPE_CONTRAT, default='I')
    GRADE = (
        ('1', 'Junior'),
        ('2', 'Confirmé'),
        ('3', 'Sénior'),
        ('4', 'Expert'),
    )
    grade = models.CharField(max_length=1, choices=GRADE, default='1')
    dateArrivee = models.DateField('date d\'arrivée chez Themis', null=True)
    dateSortie = models.DateField('date de sortie de chez Themis', blank=True, null=True)
    expertiseSectorielle = models.ManyToManyField(expertiseSectorielle)
    niveauxIntervention = models.ManyToManyField(niveauIntervention)
    expSignificative1= models.CharField(max_length=500, blank=True, null=True)
    expSignificative2= models.CharField(max_length=500, blank=True, null=True)
    expSignificative3= models.CharField(max_length=500, blank=True, null=True)
    expSignificative4= models.CharField(max_length=500, blank=True, null=True)
    expSignificative5= models.CharField(max_length=500, blank=True, null=True)
    clientPrincipaux = models.ManyToManyField(client)
    listeCompetencesCles = models.ManyToManyField(competences)
    formation = models.ManyToManyField(obtentionFormation)
    parcours = models.TextField()
    methodologie = models.TextField()
    langues = models.ManyToManyField(LanguesParlee)
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
    dateDebut = models.DateField('date de début de mission')
    dateFin = models.DateField('date de fin de mission', blank=True, null=True)
    employeurIntervention = models.CharField(max_length=300,default='')
    mandataire = models.CharField(max_length=300,default='')
    service = models.CharField(max_length=300,default='')
    resumeIntervention = models.TextField(default='')
    descriptifMission = models.TextField(default='')
    pourcentageIntervention = models.IntegerField(default=100, validators=[MaxValueValidator(100),MinValueValidator(1)])
    environnementMission =  models.TextField(default='')
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