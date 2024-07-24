from typing import Any
from django.shortcuts import render
from center.models import Center, Storage
from center.forms import CenterForm, StorageForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic

def center_list(request):
    objects = Center.objects.all()
    context = {
        "center": objects,
    }
    return render(request, "center/center-list.html", context)

def center_detail(request, id):
    object = Center.objects.get(id=id)
    context = {
        "center": object,
    }
    return render(request, "center/center-detail.html", context)

def create_center(request):
    if request.method == "POST":
        form = CenterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("center:list"))
        return render(request, "center/create-center.html", {"form": form})
    # GET
    context = {
        "form": CenterForm()
    }
    return render(request, "center/create-center.html", context)

def update_center(request, id):
    try:
        center = Center.objects.get(id=id)
    except Center.DoesNotExist:
        raise Http404("Center instance is not found")
    
    if request.method == "POST":
        form = CenterForm(request.POST, instance = center)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("center:detail", kwargs={"id": center.id}))
        return render(request, "center/update-center.html", {"form": form})
    # Get
    context = {
        "form": CenterForm(instance = center)
    }
    return render(request, "center/update-center.html", context)

def delete_center(request, id):
    try:
        center = Center.objects.get(id=id)
    except Center.DoesNotExist:
        raise Http404("Center instance not found")
    
    if request.method == "POST":
        center.delete()
        return HttpResponseRedirect(reverse("center:list"))
    # GET
    context = {
        "center": center,
    }
    return render(request, "center/delete-center.html", context)


class StorageList(generic.ListView):
    queryset = Storage.objects.all()
    template_name = "storage/storage-list.html"

    def get_queryset(self):
        return super().get_queryset().filter(center_id = self.kwargs["center_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["center_id"] = self.kwargs["center_id"]
        return context

class StorageDetail(generic.DetailView):
    model = Storage
    template_name = "storage/storage-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_quantity"] = self.object.total_quantity - self.object.booked_quantity
        return context

class CreateStorage(generic.CreateView):
    model = Storage
    form_class = StorageForm
    template_name = "storage/storage-create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["center_id"] = self.kwargs["center_id"]
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        initial["center"] = Center.objects.get(id=self.kwargs["center_id"])
        return initial
    
    def get_success_url(self):
        return reverse("center:storage-list", kwargs={"center_id": self.kwargs["center_id"]})


class StorageUpdate(generic.UpdateView):
    model = Storage
    form_class = StorageForm
    template_name = "storage/storage-update.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["center_id"] = self.get_object().center.id
        return kwargs
    
    def get_success_url(self) -> str:
        return reverse("center:storage-list", kwargs={"center_id": self.get_object().center.id})

class StorageDelete(generic.DeleteView):
    model = Storage
    template_name = "storage/storage-delete.html"

    def get_success_url(self) -> str:
        return reverse("center:storage-list", kwargs={"center_id": self.get_object().center.id})