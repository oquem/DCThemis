from django.contrib import admin

# Register your models here.
from .models import competences, familleCompetences, outils, familleOutils, collaborateurs, experiences, client, projet, BU, gestionManagerialeProjet, gestionCommercialeProjet, gestionManagerialeConsultant, expertiseSectorielle, formation, obtentionFormation, niveauIntervention, LanguesParlee

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
    search_fields = ['outilsCollaborateur__nomOutil','listeCompetencesCles__nomCompetence']
    list_filter = ('estEnIntercontrat','nbAnneeExperience','manager','typeContrat')
    list_display = ('nomCollaborateur', 'prenomCollaborateur', 'titreCollaborateur')
    view_on_site = True
admin.site.register(collaborateurs, CollabAdmin)
class ExpeAdmin(admin.ModelAdmin):
    search_fields = ['collaborateurMission__nomCollaborateur','collaborateurMission__prenomCollaborateur']
    list_filter = ('employeurIntervention','collaborateurMission__nomCollaborateur')
    view_on_site = True
admin.site.register(experiences, ExpeAdmin)
class ProjetAdmin(admin.ModelAdmin):
    search_fields = ['client','nomProjet']
    list_filter = ('client','experiencesLiees__collaborateurMission__nomCollaborateur','nbJourHomme')
    list_display = ('nomProjet', 'nbJourHomme')
admin.site.register(projet, ProjetAdmin)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ['nomClient']
    list_filter = ('domaineClient',)
admin.site.register(client,ClientAdmin)
admin.site.register(BU)
admin.site.register(gestionManagerialeProjet)
admin.site.register(gestionCommercialeProjet)
admin.site.register(gestionManagerialeConsultant)
admin.site.register(expertiseSectorielle)
admin.site.register(formation)
admin.site.register(obtentionFormation)
admin.site.register(niveauIntervention)
admin.site.register(LanguesParlee)