from django.contrib import admin

from huscy.attributes import models
from huscy.attributes.services import _create_attribute_category_permissions


class AttributeSchemaAdmin(admin.ModelAdmin):
    def save_model(self, request, attribute_schema, form, change):
        super().save_model(request, attribute_schema, form, change)
        _create_attribute_category_permissions(attribute_schema.schema)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.AttributeSchema, AttributeSchemaAdmin)
