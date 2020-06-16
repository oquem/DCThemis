from django.db import models
from django.forms import ModelForm
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField 

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
        ('6B','Assurance de Personne'),
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
        ('3D','Industrie'),
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
    def __str__(self):
        return self.nomClient

#Methodo
class Methodo(models.Model):
    nom = models.CharField(max_length=250)
    def __str__(self):
        return self.nom
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
        ('Intermediaire','Intermediaire'),
        ('Professionnel','Professionnel'),
        ('Courant','Courant'),
        ('Bilingue', 'Bilingue'),
    )
    niveau = models.CharField(max_length=20, choices=NIVEAU_LANGUE, default='Debutant')
    def __str__(self):
        return str('%s %s' %(self.nom, self.niveau))

#Collaborateur
class collaborateurs(models.Model):
    nomCollaborateur = models.CharField('Nom du Collaborateur', max_length=200)
    prenomCollaborateur = models.CharField('Prénom du Collaborateur', max_length=200)
    trigramme = models.CharField(max_length=3,blank=True, null=True)
    titreCollaborateur = models.CharField('Titre du Collaborateur',max_length=200, help_text="Il s’agit du titre que l’on retrouve en première page du DC au-dessus du texte introductif (ex : Consultant AMOA)")
    dateDeNaissance = models.DateField('Date de naissance', blank=True, null=True)
    texteIntroductifCv = RichTextField('Texte introductif du DC', default='',blank=True, null=True, help_text="Il s’agit du texte introductif que l’on retrouve en première page du DC au-dessous du titre introductif")
    nbAnneeExperience = models.IntegerField('Nb d’année d’expérience', blank=True, null=True)
    codePostal = models.CharField('Code Postal', default='',max_length=200,blank=True, null=True)
    telephone = models.CharField('Téléphone', default='',max_length=200,blank=True, null=True)
    mail = models.CharField(default='',max_length=200,blank=True, null=True)
    manager = models.ManyToManyField(gestionManagerialeConsultant)
    TYPE_CONTRAT = (
        ('I', 'CDI'),
        ('D', 'CDD'),
        ('N', 'Intérimaire'),
        ('A', 'Contrat d\'alternance'),
        ('X', 'Indépendant'),
        ('S', 'Sous-traitant'),
    )
    typeContrat = models.CharField('Type de Contrat', max_length=1, choices=TYPE_CONTRAT, default='I')
    GRADE = (
        ('1', 'Junior'),
        ('2', 'Confirmé'),
        ('3', 'Sénior'),
        ('4', 'Expert'),
    )
    grade = models.CharField(max_length=1, choices=GRADE, default='1',blank=True, null=True)
    dateArrivee = models.DateField('date d\'arrivée chez Themis', blank=True, null=True)
    dateSortie = models.DateField('date de sortie de chez Themis', blank=True, null=True)
    expertiseSectorielle = models.ManyToManyField(expertiseSectorielle, blank=True, verbose_name='Expertise Sectorielle',help_text='Indique le « secteur : Direction ou Service Client » (ex : Industrie Pharmaceutique : Achat, Service Financier)')
    niveauxIntervention = models.ManyToManyField(niveauIntervention, blank=True, verbose_name='Niveau d’intervention',help_text='Idéalement en indiquer 5 et en ne dépassant pas les 10')
    expSignificative1= models.CharField('Expérience Significative 1', max_length=500, blank=True, null=True)
    expSignificative2= models.CharField('Expérience Significative 2', max_length=500, blank=True, null=True)
    expSignificative3= models.CharField('Expérience Significative 3', max_length=500, blank=True, null=True)
    expSignificative4= models.CharField('Expérience Significative 4', max_length=500, blank=True, null=True)
    expSignificative5= models.CharField('Expérience Significative 5', max_length=500, blank=True, null=True)
    clientPrincipaux = models.ManyToManyField(client, blank=True, verbose_name='Clients Principaux', help_text='Idéalement en indiquer 5 et en ne dépassant pas les 10')
    listeCompetencesCles = models.ManyToManyField(competences, blank=True, verbose_name='Compétences Clés ')
    formation = models.ManyToManyField(obtentionFormation, blank=True)
    parcours = RichTextField(default='', blank=True)
    methodologie = models.ManyToManyField(Methodo, blank=True, verbose_name='Méthodologies')
    langues = models.ManyToManyField(LanguesParlee, blank=True, help_text='Obligatoire, indiquez le niveau d’anglais')
    outilsCollaborateur = models.ManyToManyField(outils, blank=True, verbose_name='Outils')
    estEnIntercontrat = models.BooleanField(default=False)
    def __str__(self):
        return self.nomCollaborateur
    def get_absolute_url(self):
        return "/consultant/%i/" % self.id
    class Meta: 
        verbose_name = 'Consultant'

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
    projetThemis = models.BooleanField('Projet Thémis', default=True, help_text="Décochez la coche, s’il s’agit d’un projet pour le compte d’une autre société")
    nomProjet = models.CharField('Nom du projet', max_length=300)
    client = models.ForeignKey(client, on_delete=models.CASCADE, null=True)
    budget = models.DecimalField(decimal_places=2,max_digits=11, default=0.0, blank=True)
    nbJourHomme = models.IntegerField('Nombre de jours hommes', blank=True)
    dateDebut = models.DateField('date de début du Projet', null=True)
    dateFin = models.DateField('date de fin du Projet', blank=True, null=True)
    resumeProjet = RichTextField('Résumé du Projet', default='', blank=True, null=True, help_text='Bref résumé du projet en 3 lignes')
    contexteMission = RichTextField('Contexte et Enjeux', default='', blank=True, null=True)
    demarcheenjeux = RichTextField('Démarche et réalisations', default='', blank=True, null=True, help_text='Merci d’y ajouter aussi l’environnement technique de la mission')
    livrables = RichTextField(default='', blank=True, null=True, help_text='Listez les livrables sous forme de bullet point')
    benefClient = RichTextField('Bénéfices Client',default='', blank=True, null=True, help_text='Se mettre à la place du client et lister les bénéfices obtenus')
    BUProjet = models.ForeignKey(BU, on_delete=models.SET_NULL, null=True, verbose_name='BU rattaché au projet')
    gestionManageriale = models.ManyToManyField(gestionManagerialeProjet, blank=True, verbose_name='Gestion Managériale', help_text="Indiquez le nom du Manager responsable du projet")
    gestionCommerciale = models.ManyToManyField(gestionCommercialeProjet, blank=True, verbose_name='Gestion Commerciale', help_text="Indiquez le nom du Commercial responsable du projet")
    #experiencesLiees = models.ManyToManyField(experiences)
    def __str__(self):
        return self.nomProjet


#Experiences
class experiences(models.Model):
    missionThemis = models.BooleanField('Mission Thémis', default=True, help_text="Décochez la coche, s’il s’agit d’une mission pour le compte d’une autre société")
    nomMission = models.CharField('Niveau d’intervention', max_length=300, help_text="Indiquez le poste occupé par le consultant lors de l’intervention ex : (Consultant BI)")
    dateDebut = models.DateField('date de début de mission')
    dateFin = models.DateField('date de fin de mission', blank=True, null=True)
    employeur = models.CharField('Employeur lors de l’intervention', max_length=300,default='', blank=True, help_text="Dans le cas où la coche est décochée, merci d’indiquer pour le compte de quelle société avez-vous effectué cette intervention ?")
    mandataire = models.CharField(max_length=300,default='',blank=True, help_text="Si vous êtes passez par un intermédiaire, merci d’indiquer le nom de la société sous-traitante (ex :Eugena)")
    service = models.CharField('Direction ou Service Client', max_length=300,default='',blank=True, help_text='Indiquez le la Direction ou le Service du client dans lequel le consultant est intervenu')
    resumeIntervention =  RichTextField('Contexte de l’intervention', default='', blank=True)
    descriptifMission =  RichTextField('Descriptif de la mission', default='', blank=True, help_text='Décrire l’intervention en détail')
    environnementMission =  RichTextField('Environnement Technique', default='', blank=True, null=True)
    pourcentageIntervention = models.IntegerField('Pourcentage du temps passé en intervention', default=100, validators=[MaxValueValidator(100),MinValueValidator(1)],blank=True)
    collaborateurMission = models.ForeignKey(collaborateurs, on_delete=models.CASCADE, default='', verbose_name='Collaborateur', help_text='Utilisez la liste pour rattacher le collaborateur à la mission')
    projetDeLaMission = models.ForeignKey(projet, on_delete=models.SET_NULL, default='', null=True, verbose_name='Projet de la mission')
    def __str__(self):
        return self.nomMission
    def get_absolute_url(self):
        collab=self.collaborateurMission.id
        return "/consultant/%i/" % collab
    class Meta: 
        verbose_name = 'Intervention'
