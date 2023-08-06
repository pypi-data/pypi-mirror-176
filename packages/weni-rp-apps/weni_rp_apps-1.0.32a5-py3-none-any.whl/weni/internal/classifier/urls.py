from rest_framework import routers

from .views import ClassifierEndpoint


router = routers.SimpleRouter()
router.register("classifier", ClassifierEndpoint, basename="classifier")

<<<<<<< HEAD
urlpatterns = router.urls
=======
urlpatterns = format_suffix_patterns(router.urls, allowed=["json", "api"])
>>>>>>> cec6b42... fix: is_active_filter
