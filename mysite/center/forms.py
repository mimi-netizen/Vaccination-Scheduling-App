from django.forms import ModelForm
from center.models import Center, Storage

class CenterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CenterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Center
        fields = "__all__"

class StorageForm(ModelForm):
    def __init__(self, center_id, *args, **kwargs):
        super(StorageForm, self).__init__(*args, **kwargs)
        self.fields["center"].queryset = Center.objects.filter(id=center_id)
        self.fields["center"].disabled = True
        self.fields["booked_quantity"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Storage
        fields = "__all__"