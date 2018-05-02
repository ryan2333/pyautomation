#-*- coding: utf-8 -*-

from django.forms import ModelForm
from .models import AssetCategory, AssetIDC, AssetVendor, PhysicalDevice

class AssetCategoryForm(ModelForm):
    class Meta:
        model = AssetCategory
        fields = "__all__"


class AssetIDCForm(ModelForm):
    class Meta:
        model = AssetIDC
        fields = "__all__"


class AssetVendorForm(ModelForm):
    class Meta:
        model = AssetVendor
        fields = "__all__"


class PhysicalDeviceForm(ModelForm):
    class Meta:
        model = PhysicalDevice
        fields = "__all__"
