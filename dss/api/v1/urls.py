from rest_framework.routers import DefaultRouter
from dss.api.v1 import viewsets

app_name = 'dss'
router = DefaultRouter()
router.register(r'folder', viewsets.FolderViewset, basename='folder')
router.register(r'document', viewsets.DocumentViewset, basename='document')
router.register(r'topic', viewsets.TopicViewset, basename='topic')
router.register(r'doc/topic', viewsets.DocTopicViewset, basename='doc-topic')
urlpatterns = router.urls
