from django.urls import path
from rest_framework.routers import DefaultRouter
from myapp import views


router = DefaultRouter()
router.register('book', views.BookViewSet)
router.register('book2', views.BookViewSet2)

urlpatterns = [
    # path('get-post-person', views.person_view),
    # path('get-post-car', views.car_view),
    # path('information', views.information_view)
]

urlpatterns += router.urls