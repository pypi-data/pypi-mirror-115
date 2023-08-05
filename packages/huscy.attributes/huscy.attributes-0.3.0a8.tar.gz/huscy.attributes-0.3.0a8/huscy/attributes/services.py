import jsonschema
from django.db.transaction import atomic
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from huscy.attributes.models import AttributeSchema, AttributeSet
from huscy.pseudonyms.services import get_or_create_pseudonym


@atomic
def create_attribute_schema(schema):
    _create_attribute_category_permissions(schema)
    return AttributeSchema.objects.create(schema=schema)


def _create_attribute_category_permissions(schema):
    content_type = ContentType.objects.get_for_model(AttributeSchema)

    for name, value in schema['properties'].items():
        if value['type'] == 'object':
            Permission.objects.get_or_create(
                codename=f'change_attribute_category_{name}',
                name=f'Can Change Attribute Category {name}',
                content_type=content_type
            )
            Permission.objects.get_or_create(
                codename=f'view_attribute_category_{name}',
                name=f'Can View Attribute Category {name}',
                content_type=content_type
            )


def get_or_create_attribute_set(subject):
    pseudonym = get_or_create_pseudonym(subject, 'attributes.attributeset')

    attribute_set, created = AttributeSet.objects.get_or_create(pseudonym=pseudonym.code)
    return attribute_set


def update_attribute_set(attribute_set, attributes, attribute_schema_version=None):
    if attribute_schema_version is None:
        attribute_schema = attribute_set.attribute_schema
    else:
        if attribute_schema_version < attribute_set.attribute_schema.pk:
            raise Exception('New version for attribute schema must be greater than or equals with '
                            'current attribute schema version.')
        attribute_schema = AttributeSchema.objects.get(pk=attribute_schema_version)

    jsonschema.validate(attributes, attribute_schema.schema)

    attribute_set.attributes = attributes
    attribute_set.attribute_schema = attribute_schema
    attribute_set.save()

    return attribute_set


def get_attribute_schema(version=None):
    queryset = AttributeSchema.objects

    try:
        if version is None:
            return queryset.latest('pk')
        else:
            return queryset.get(pk=version)
    except AttributeSchema.DoesNotExist:
        return _create_initial_attribute_schema()


def _create_initial_attribute_schema():
    if AttributeSchema.objects.exists():
        raise Exception('Initial attribute schema already exist!')
    return create_attribute_schema(dict(type='object', properties=dict()))
