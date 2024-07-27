from django.contrib import admin
from campaign.models import Campaign, Slot

class SlotInline(admin.TabularInline):
    model = Slot
    readonly_fields = ["reserved"]


class CustomCampaignAdmin(admin.ModelAdmin):
    inlines = [SlotInline]
    search_fields = ["vaccine__name", "center__name"]
    list_display = ["vaccine", "center", "start_date", "end_date"]
    ordering = ["-start_date"]
    fields = (
        ("vaccine"),
        ("center"),
        ("start_date", "end_date"),
        ("agents"),
    )


admin.site.register(Campaign, CustomCampaignAdmin)
