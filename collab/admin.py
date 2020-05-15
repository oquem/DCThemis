from django.contrib import admin

# Register your models here.
from .models import competences, familleCompetences, outils, familleOutils, collaborateurs, experiences, domaine, client, projet

class CompetenceAdmin(admin.ModelAdmin):
    search_fields = ['nomCompetence']
    list_filter = ('famille',)
admin.site.register(competences, CompetenceAdmin)
admin.site.register(familleCompetences)
class OutilAdmin(admin.ModelAdmin):
    search_fields = ['nomOutil']
    list_filter = ('famille',)
admin.site.register(outils, OutilAdmin)
admin.site.register(familleOutils)
class CollabAdmin(admin.ModelAdmin):
    search_fields = ['outilsCollaborateur__nomOutil','listeCompetencesCles__nomCompetence']
    list_filter = ('estEnIntercontrat','nbAnneeExperience')
    list_display = ('nomCollaborateur', 'prenomCollaborateur', 'titreCollaborateur')
    view_on_site = True
admin.site.register(collaborateurs, CollabAdmin)
class ExpeAdmin(admin.ModelAdmin):
    search_fields = ['collaborateurMission__nomCollaborateur','collaborateurMission__prenomCollaborateur']
    list_filter = ('client','collaborateurMission__nomCollaborateur')
    view_on_site = True
admin.site.register(experiences, ExpeAdmin)
class ProjetAdmin(admin.ModelAdmin):
    search_fields = ['experiencesLiees__client__nomClient','nomProjet']
    list_filter = ('experiencesLiees__client__nomClient','experiencesLiees__collaborateurMission__nomCollaborateur','nbJourHomme')
    list_display = ('nomProjet', 'nbJourHomme')
admin.site.register(projet, ProjetAdmin)
admin.site.register(domaine)
admin.site.register(client)