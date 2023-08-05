from rest_framework import serializers

from huscy.attributes import models
from huscy.attributes.services import create_attribute_schema, update_attribute_set


class AttributeSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeSchema
        fields = (
            'created_at',
            'id',
            'schema',
        )
        read_only_fields = 'created_at',

    def create(self, validated_data):
        return create_attribute_schema(**validated_data)


class AttributeSetSerializer(serializers.ModelSerializer):
    attribute_schema = AttributeSchemaSerializer(read_only=True)
    attributes = serializers.JSONField()

    class Meta:
        model = models.AttributeSet
        fields = (
            'attribute_schema',
            'attributes',
        )

    def update(self, attribute_set, validated_data):
        return update_attribute_set(attribute_set, **validated_data)
