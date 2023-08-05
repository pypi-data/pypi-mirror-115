from rest_framework import generics, mixins, permissions, viewsets

from huscy.attributes import models, serializer, services
from huscy.attributes.permissions import AttributeSetPermission
from huscy.subjects.models import Subject


class AttributeSchemaView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                          generics.GenericAPIView):
    permission_classes = (permissions.DjangoModelPermissions, )
    queryset = models.AttributeSchema.objects.all()
    serializer_class = serializer.AttributeSchemaSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_object(self):
        return services.get_attribute_schema()


class AttributeSetViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, AttributeSetPermission)
    queryset = Subject.objects.all()
    serializer_class = serializer.AttributeSetSerializer

    def get_object(self):
        subject = super().get_object()
        return services.get_or_create_attribute_set(subject)
