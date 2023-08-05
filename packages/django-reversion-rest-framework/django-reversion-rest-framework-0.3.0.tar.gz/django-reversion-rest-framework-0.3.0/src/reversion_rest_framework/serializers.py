from rest_framework import serializers
from reversion.models import Revision, Version


class RevisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Revision
        fields = ('date_created', 'user', 'comment')


class VersionSerializer(serializers.ModelSerializer):
    revision = RevisionSerializer(read_only=True)

    class Meta:
        model = Version
        fields = ('revision', 'field_dict',)
        # fields = ('id', 'revision', 'field_dict',)
