from django.contrib import admin

# Register your models here.
from .models import competences, familleCompetences, outils, familleOutils, collaborateurs, experiences, client, projet, BU, gestionManagerialeProjet, gestionCommercialeProjet, gestionManagerialeConsultant, expertiseSectorielle, formation, obtentionFormation, niveauIntervention, LanguesParlee, Methodo

class CompetenceAdmin(admin.ModelAdmin):
    search_fields = ['nomCompetence']
    list_display = ('nomCompetence','famille')
    list_filter = ('famille',)
admin.site.register(competences, CompetenceAdmin)
admin.site.register(familleCompetences)
class OutilAdmin(admin.ModelAdmin):
    search_fields = ['nomOutil']
    list_display = ('nomOutil','famille')
    list_filter = ('famille',)
admin.site.register(outils, OutilAdmin)
admin.site.register(familleOutils)
class CollabAdmin(admin.ModelAdmin):
    search_fields = ['outilsCollaborateur__nomOutil','listeCompetencesCles__nomCompetence','nomCollaborateur', 'prenomCollaborateur',]
    list_filter = ('estEnIntercontrat','manager__manager','typeContrat','grade','methodologie')
    list_display = ('nomCollaborateur', 'prenomCollaborateur', 'titreCollaborateur','typeContrat')
    view_on_site = True
admin.site.register(collaborateurs, CollabAdmin)
class ExpeAdmin(admin.ModelAdmin):
    search_fields = ['collaborateurMission__nomCollaborateur','collaborateurMission__prenomCollaborateur','mandataire','service','nomMission','projetDeLaMission__client__nomClient']
    list_filter = ('collaborateurMission__nomCollaborateur','mandataire','projetDeLaMission__client','missionThemis','projetDeLaMission')
    list_display = ('nomMission', 'collaborateurMission', 'projetDeLaMission')
    view_on_site = True
admin.site.register(experiences, ExpeAdmin)
class ProjetAdmin(admin.ModelAdmin):
    search_fields = ['client','nomProjet']
    list_filter = ('client','nbJourHomme','projetThemis')
    list_display = ('nomProjet','client','nbJourHomme')
admin.site.register(projet, ProjetAdmin)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ['nomClient']
    list_filter = ('domaineClient',)
admin.site.register(client,ClientAdmin)
admin.site.register(BU)
class gestionManagerialeProjetAdmin(admin.ModelAdmin):
    search_fields = ['manager']
    list_filter = ('manager','dateDebut','dateFin')
admin.site.register(gestionManagerialeProjet, gestionManagerialeProjetAdmin)
class gestionCommercialeProjetAdmin(admin.ModelAdmin):
    search_fields = ['manager']
    list_filter = ('manager','dateDebut','dateFin')
admin.site.register(gestionCommercialeProjet, gestionCommercialeProjetAdmin)
class gestionManagerialeConsultantAdmin(admin.ModelAdmin):
    search_fields = ['manager']
    list_filter = ('manager','dateDebut','dateFin')
admin.site.register(gestionManagerialeConsultant, gestionManagerialeConsultantAdmin)
admin.site.register(expertiseSectorielle)
class FormationAdmin(admin.ModelAdmin):
    search_fields = ['diplome','ecole']
    list_filter = ('ecole','diplome')
admin.site.register(formation, FormationAdmin)
admin.site.register(obtentionFormation)
admin.site.register(niveauIntervention)
admin.site.register(LanguesParlee)
admin.site.register(Methodo)