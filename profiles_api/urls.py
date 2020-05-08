from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile',views.UserProfileViewSet,basename="UserProfileViewSet")
router.register('worker_to_manager_req',views.WorkerToManagerReq,basename="WorkerToManagerReq")
router.register('worker_to_orgworker_req',views.WorkerToOrgWorkerReq,basename="WorkerToOrgWorkerReq")
router.register('orgworker_to_manager_req',views.OrgWorkerToManagerReq,basename="OrgWorkerToManagerReq")
router.register('organization',views.OrganizationViewSet,basename="OrganizationViewSet")
router.register('duty',views.DutyViewSet,basename="DutyViewSet")
urlpatterns = [
    path('', include(router.urls)),
    path('login/',views.UserLoginApiView.as_view()),
    path('accept/<int:reqID>/',views.Accept.as_view(), name='accept'),
    path('reject/<int:reqID>/',views.Reject.as_view(), name='reject')
]