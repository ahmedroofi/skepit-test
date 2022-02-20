from django.db.models import Q
from rest_framework import serializers
from dss.models import Folder, Document, Topic
from users.api.v1.serializers import PublicUserSerializer


class FolderSerializer(serializers.ModelSerializer):
    """
    Folder Serializer
    """

    created_by = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = "__all__"

    def create(self, validated_data):
        user = self.context.get("user")
        validated_data["created_by"] = user
        folder = super(FolderSerializer, self).create(validated_data)
        return folder

    def get_created_by(self, obj):
        return PublicUserSerializer(obj.created_by).data

    def get_documents(self, obj):
        doc_q = self.context.get("doc_q")
        tpc_q = self.context.get("tpc_q")
        docs = obj.documents.all()
        if doc_q:
            docs = docs.filter(name__icontains=doc_q)
        if tpc_q:
            docs = docs.filter(Q(topics__title__icontains=tpc_q) | Q(
                topics__description__icontains=tpc_q)).distinct()
        return DocumentSerializer(docs, many=True).data


class DocumentSerializer(serializers.ModelSerializer):
    """
    Document Serializer
    """

    created_by = serializers.SerializerMethodField()
    topics = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = "__all__"

    def create(self, validated_data):
        user = self.context.get("user")
        validated_data["created_by"] = user
        doc = super(DocumentSerializer, self).create(validated_data)
        return doc

    def get_created_by(self, obj):
        return PublicUserSerializer(obj.created_by).data

    def get_topics(self, obj):
        topics = obj.topics.all()
        return TopicSerializer(topics, many=True).data


class TopicSerializer(serializers.ModelSerializer):
    """
    Topic Serializer
    """

    class Meta:
        model = Topic
        fields = ("id", "title",)


class DetailTopicSerializer(serializers.ModelSerializer):
    """
    Topic Serializer
    """
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = "__all__"

    def create(self, validated_data):
        user = self.context.get("user")
        validated_data["created_by"] = user
        doc = super(DetailTopicSerializer, self).create(validated_data)
        return doc

    def get_created_by(self, obj):
        return PublicUserSerializer(obj.created_by).data
