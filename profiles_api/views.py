from . import models,serializers
from rest_framework import viewsets,status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from . import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Roll
from datetime import datetime,timedelta




class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.roll == models.Roll.MANAGER:
            return models.UserProfile.objects.filter(organization=user.organization,roll = models.Roll.ORG_WORKER)
        elif user.is_authenticated and user.roll == models.Roll.ADMIN:
            return models.UserProfile.objects.all()
        elif user.is_authenticated and user.roll == Roll.ORG_WORKER:
            return models.UserProfile.objects.filter(id = user.id)
        elif user.is_authenticated and user.roll == Roll.WORKER:
            return models.UserProfile.objects.filter(id = user.id)
        return None
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.roll == Roll.MANAGER:
            instance = self.get_object()
            instance.roll = Roll.WORKER
            instance.save()
            models.Request.objects.filter(from_user__id = instance.id).delete()
            return Response({"successful":"the "+instance.name+" fired from organization!"})


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class WorkerToManagerReq(viewsets.ModelViewSet):
    serializer_class = serializers.WKtoMANSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,permissions.WorkerToManagerPermission,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.roll == models.Roll.WORKER:
            return models.Request.objects.filter(from_user=user.id,to_see=Roll.ADMIN,job_title=Roll.MANAGER)
        elif user.is_authenticated and user.roll == models.Roll.ADMIN:
            return models.Request.objects.filter(to_see=Roll.ADMIN,job_title=Roll.MANAGER)
        return None

class WorkerToOrgWorkerReq(viewsets.ModelViewSet):
    serializer_class = serializers.WKtoORGWKSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,permissions.WorkerToOrgeWorkerPermission,)
    def get_queryset(self):

        user = self.request.user

        if user.roll == Roll.MANAGER:
            return models.Request.objects.filter(to_see=Roll.MANAGER,job_title=Roll.ORG_WORKER
                                                 ,from_user__roll=Roll.WORKER,organization=user.organization.id)
        elif user.roll == Roll.WORKER:
            return  models.Request.objects.filter(from_user=user.id,to_see=Roll.MANAGER,job_title=Roll.ORG_WORKER)
        else:
            return None


class OrgWorkerToManagerReq(viewsets.ModelViewSet):
    serializer_class = serializers.OWtoMANSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,permissions.OrgWorkerToManagerPermission,)
    def get_queryset(self):

        user = self.request.user

        if user.roll == Roll.MANAGER:
            return models.Request.objects.filter(to_see=Roll.MANAGER,job_title=models.Roll.MANAGER
                                                 ,from_user__roll=Roll.ORG_WORKER,organization=user.organization.id)
        elif user.roll == Roll.ORG_WORKER:
            return models.Request.objects.filter(from_user=user.id,to_see=Roll.MANAGER,job_title=Roll.MANAGER)
        else:
            return None


class Accept(APIView):
    serializer_class = serializers.RequestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self,request,reqID):
        user = request.user
        if user.is_authenticated and user.roll == Roll.MANAGER:
            req = models.Request.objects.filter(id = reqID)
            if len(req) == 0:
                return Response({"error":"there is no such a req ID"})
            req = req[0]
            if (req.from_user.roll == Roll.ORG_WORKER) and (req.job_title==Roll.MANAGER) and (req.organization == user.organization):
                requester = req.from_user
                requester.roll = Roll.MANAGER
                requester.save()
                models.Request.objects.filter(from_user__id = requester.id).delete()
                return Response({"successfull":"request Accepted and "+requester.name+" is now one ofthe managers of your organization!"})
            elif (req.from_user.roll == Roll.WORKER) and (req.job_title==Roll.ORG_WORKER) and (req.organization == user.organization):
                requester = req.from_user
                requester.roll = Roll.ORG_WORKER
                requester.organization = user.organization
                requester.save()
                models.Request.objects.filter(from_user__id=requester.id,job_title=Roll.ORG_WORKER).delete()
                models.Request.objects.filter(from_user__id=requester.id, job_title=Roll.MANAGER).exclude(organization = requester.organization).delete()
                manReqs = models.Request.objects.filter(from_user__id = requester.id, job_title = Roll.MANAGER,organization = requester.organization)
                if len(manReqs) == 1:
                    print("are")
                    req = manReqs[0]
                    req.to_see = Roll.MANAGER
                    req.save()
                return Response({"successfull": "request Accepted and " + requester.name + " is now one ofthe managers of your organization!"})
            else:
                return Response({"error":"you dont have permission to Accept this request"})
        elif user.is_authenticated and user.roll == Roll.ADMIN:
            req = models.Request.objects.filter(id=reqID)
            if len(req) == 0:
                return Response({"error": "there is no such a req ID"})
            req = req[0]
            if (req.from_user.roll == Roll.WORKER) and (req.job_title == Roll.MANAGER):
                requester = req.from_user
                requester.roll = Roll.MANAGER
                requester.organization = req.organization
                requester.save()
                models.Request.objects.filter(from_user__id=requester.id).delete()
                return Response({
                                    "successfull": "request Accepted and " + requester.name + " is now one ofthe managers of organization!"})

        return Response({"message":"you are not allow to do this operation!"})


class Reject(APIView):
    serializer_class = serializers.RequestSerializer
    authentication_classes = (TokenAuthentication,)
    def get(self,request,reqID):
        user = request.user
        if user.is_authenticated and user.roll == Roll.MANAGER:

            req = models.Request.objects.filter(id = reqID)
            if len(req) == 0:
                return Response({"error":"there is no such a req ID"})
            req = req[0]
            if (req.from_user.roll == Roll.ORG_WORKER) and (req.job_title==Roll.MANAGER) and (req.organization == user.organization):
                req.delete()
                return Response({"successfull":"request Rejected!"})
            elif (req.from_user.roll == Roll.WORKER) and (req.job_title == Roll.ORG_WORKER) and (req.organization == user.organization):
                req.delete()
                return Response({"successfull":"request Rejected!"})
            else:
                return Response({"error":"you dont have permission to Reject this request"})
        elif user.is_authenticated and user.roll == Roll.ADMIN:
            req = models.Request.objects.filter(id=reqID)
            if len(req) == 0:
                return Response({"error": "there is no such a req ID"})
            req = req[0]
            if (req.from_user.roll == Roll.WORKER) and (req.job_title == Roll.MANAGER):
                req.delete()
                return Response({"successfull": "request rejected!!"})
        return Response({"message":"unkown"})

class DutyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DutySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.DutyPermission,IsAuthenticated,)
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.roll == models.Roll.MANAGER:
            return models.duty.objects.filter(organization=user.organization).order_by('deadline')
        elif user.is_authenticated and user.roll == models.Roll.ADMIN:
            return models.duty.objects.all().order_by('deadline')
        elif user.is_authenticated and user.roll == Roll.ORG_WORKER:
            return models.duty.objects.filter(organization=user.organization , persons__id = user.id).order_by('deadline')
        return None

class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrganizationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,permissions.EditOrganizationPermission,)

    def get_queryset(self):
        user = self.request.user
        if user.roll == Roll.ADMIN:
            return models.Organization.objects.all()
        else:
            return None
