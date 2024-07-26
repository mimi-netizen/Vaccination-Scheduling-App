from django.forms import ModelForm
from campaign.models import Campaign, Slot

class CampaignForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Campaign
        fields = "__all__"

class SlotForm(ModelForm):
    def __init__(self, campaign_id, *args, **kwargs):
        super(SlotForm, self).__init__(*args, **kwargs)
        self.fields["campaign"].queryset = Campaign.objects.filter(id=campaign_id)
        self.fields["campaign"].disabled = True
        self.fields["reserved"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Slot
        fields = "__all__"