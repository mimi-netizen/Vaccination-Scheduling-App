from django import forms
from vaccination.models import Vaccination

class VaccinationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VaccinationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget = forms.HiddenInput()
            
    class Meta:
        model = Vaccination
        fields = ["patient", "campaign", "slot"]
        labels = {
            "campaign": "Vaccine / Center Name",
            "slot": "Date / Slot"
        }