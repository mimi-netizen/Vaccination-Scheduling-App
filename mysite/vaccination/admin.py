from django.contrib import admin
from vaccination.models import Vaccination

class CustomVaccinationAdmin(admin.ModelAdmin):
    list_display = ["patient", "campaign", "slot", "is_vaccinated"]
    search_fields = ["patient__first_name", "patient__middle_name", "patient__last_name"]
    list_filter = ["is_vaccinated"]
    readonly_fields = [
        "patient",
        "campaign",
        "is_vaccinated",
        "updated_by",
        "date",
    ]
    change_form_template = "admin/change-vaccination.html"

admin.site.register(Vaccination, CustomVaccinationAdmin)
