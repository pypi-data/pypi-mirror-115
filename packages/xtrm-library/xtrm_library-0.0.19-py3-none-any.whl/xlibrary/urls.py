from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register('senders', viewsets.SenderViewset,base_name='sender')

urlpatterns = router.urls
