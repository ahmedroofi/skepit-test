from django.db.models import Q
from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from common.custom_response import spkt_response
from .serializers import *
from dss.models import Folder, Document, Topic


class FolderViewset(viewsets.ViewSet):

    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, format=None):
        fld = Folder.objects.all()
        serializer = FolderSerializer(fld, many=True)
        return spkt_response(serializer.data)

    def create(self, request):
        serializer = FolderSerializer(
            data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return spkt_response(serializer.data)

    def retrieve(self, request, pk=None):
        doc_q = request.GET.get("doc_q")
        tpc_q = request.GET.get("tpc_q")
        fld_obj = get_object_or_404(Folder, pk=pk)
        serializer = FolderSerializer(fld_obj, context={"doc_q": doc_q,
                                                        "tpc_q": tpc_q})
        return spkt_response(serializer.data)

    def update(self, request, pk=None):
        fld_obj = get_object_or_404(Folder, pk=pk)
        serializer = FolderSerializer(fld_obj,
                                      data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return spkt_response(serializer.data)

    def destroy(self, request, pk=None):
        fld_obj = get_object_or_404(Folder, pk=pk)
        fld_obj.delete()
        return spkt_response("Folder Deleted")


class DocumentViewset(viewsets.ViewSet):

    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, format=None):
        docs = Document.objects.all()
        doc_q = request.GET.get("doc_q")
        tpc_q = request.GET.get("tpc_q")
        if doc_q:
            docs = docs.filter(name__icontains=doc_q)
        if tpc_q:
            docs = docs.filter(Q(topics__title__icontains=tpc_q) | Q(
                topics__description__icontains=tpc_q)).distinct()
        serializer = DocumentSerializer(docs, many=True)
        return spkt_response(serializer.data)

    def create(self, request):
        serializer = DocumentSerializer(
            data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return spkt_response(serializer.data)

    def retrieve(self, request, pk=None):
        doc_obj = get_object_or_404(Document, pk=pk)
        serializer = DocumentSerializer(doc_obj)
        return spkt_response(serializer.data)

    def update(self, request, pk=None):
        doc_obj = get_object_or_404(Document, pk=pk)
        serializer = DocumentSerializer(doc_obj,
                                        data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return spkt_response(serializer.data)

    def destroy(self, request, pk=None):
        doc_obj = get_object_or_404(Document, pk=pk)
        doc_obj.delete()
        return spkt_response("Document Deleted")


class TopicViewset(viewsets.ViewSet):

    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        serializer = DetailTopicSerializer(
            data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return spkt_response(serializer.data)

    def retrieve(self, request, pk=None):
        tpc_obj = get_object_or_404(Topic, pk=pk)
        serializer = DetailTopicSerializer(tpc_obj)
        return spkt_response(serializer.data)

    def update(self, request, pk=None):
        tpc_obj = get_object_or_404(Topic, pk=pk)
        serializer = DetailTopicSerializer(tpc_obj,
                                           data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return spkt_response(serializer.data)

    def destroy(self, request, pk=None):
        tpc_obj = get_object_or_404(Topic, pk=pk)
        tpc_obj.delete()
        return spkt_response("Topic Deleted")


class DocTopicViewset(viewsets.ViewSet):

    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        doc_obj = get_object_or_404(Document, pk=pk)
        topics = doc_obj.topics.all()
        serializer = DetailTopicSerializer(topics, many=True)
        return spkt_response(serializer.data)
