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
    attributes = serializers.JSONField()

    class Meta:
        model = models.AttributeSet
        fields = (
            'attribute_schema',
            'attributes',
        )
        write_only_fields = 'attribute_schema',

    def to_representation(self, attribute_set):
        data = super().to_representation(attribute_set)
        data['attribute_schema'] = AttributeSchemaSerializer(attribute_set.attribute_schema).data
        return data

    def update(self, attribute_set, validated_data):
        return update_attribute_set(attribute_set, **validated_data)
