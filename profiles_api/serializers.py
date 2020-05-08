from rest_framework import serializers
from . import models
from .models import Roll
class UserProfileSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name= validated_data['name'],
            roll = validated_data['roll'],
            organization = validated_data['organization'],
            password= validated_data['password']
        )
        return user

    def validate(self, data):

        user = self.context['request'].user
        if not(user.is_authenticated):
            if data['organization'] != None:
                raise serializers.ValidationError("you cant choose organization as worker!")
            if data['roll'] != Roll.WORKER:
                raise serializers.ValidationError("you should as choose worker!!")
        return data

    class Meta:
        model =models.UserProfile
        fields = ('id','email','name','roll','organization','password')

        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
            }

        }



class RequestSerializer(serializers.ModelSerializer):


    class Meta:
        model =models.Request
        fields = ('id','from_user','job_title','to_see','organization')


class WKtoMANSerializer(serializers.ModelSerializer):
    job_title = serializers.ChoiceField(choices=[(Roll.MANAGER,"manager")])
    to_see = serializers.ChoiceField(choices=[(Roll.ADMIN,"admin")])

    def validate(self, data):
        print("Adadsad")
        user = self.context['request'].user
        if user.roll != Roll.WORKER:
            raise serializers.ValidationError("you are not worker and not allowed to create worker to manager request")
        if data['from_user'].id != user.id:
            raise serializers.ValidationError("you should only make request from yourself")
        reqs = models.Request.objects.filter(from_user__id = user.id, job_title = data['job_title'],to_see = data['to_see'],organization=data['organization'])
        if(len(reqs)>0):
            raise serializers.ValidationError("you already make this request")
        return data

    class Meta:
        model =models.Request
        fields = ('id','from_user','job_title','to_see','organization')

class WKtoORGWKSerializer(serializers.ModelSerializer):
    job_title = serializers.ChoiceField(choices=[(Roll.ORG_WORKER,"org_worker")])
    to_see = serializers.ChoiceField(choices=[(Roll.MANAGER,"manager")])

    def validate(self, data):

        user = self.context['request'].user
        if user.roll != Roll.WORKER:
            raise serializers.ValidationError("you are not worker and not allowed to create worker to org_worker request")
        if data['from_user'].id != user.id:
            raise serializers.ValidationError("you should only make request from yourself")
        reqs = models.Request.objects.filter(from_user__id = user.id, job_title = data['job_title'],to_see = data['to_see'],organization=data['organization'])
        if(len(reqs)>0):
            raise serializers.ValidationError("you already make this request")
        return data

    class Meta:
        model =models.Request
        fields = ('id','from_user','job_title','to_see','organization')

class OWtoMANSerializer(serializers.ModelSerializer):
    job_title = serializers.ChoiceField(choices=[(Roll.MANAGER,"manager")])
    to_see = serializers.ChoiceField(choices=[(Roll.MANAGER,"manager")])

    def validate(self, data):
        user = self.context['request'].user
        if user.roll != Roll.ORG_WORKER:
            raise serializers.ValidationError("you are not org_worker and not allowed to create org_worker to manager request")
        if data['from_user'].id != user.id:
            raise serializers.ValidationError("you should only make request from yourself")
        if data['organization'].id != user.organization.id:
            raise serializers.ValidationError("you should request for manager in your organization. change organization value!")
        reqs = models.Request.objects.filter(from_user__id = user.id, job_title = data['job_title'],to_see = data['to_see'])
        if(len(reqs)>0):
            raise serializers.ValidationError("you already make this request")
        return data

    class Meta:
        model =models.Request
        fields = ('id','from_user','job_title','to_see','organization')


class DutySerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    def validate(self, data):
        user = data['owner']
        print(user.organization)
        if data['organization'] != user.organization:
            raise serializers.ValidationError("you are tying to assign duty to another organization!")
        if user.roll == Roll.ORG_WORKER:
            persons = data['persons']
            if len(persons)>1:
                raise serializers.ValidationError("you can just assign duty to your self!")
            if len(persons) == 1:
                if persons[0].id != user.id:
                    raise serializers.ValidationError("you can just assign duty to your self!")

        if user.roll == Roll.MANAGER:
            persons = data['persons']
            flag = True
            for p in persons:
                if p.roll != Roll.ORG_WORKER or p.organization != user.organization:
                    flag = False
                    break
            if not(flag):
                raise serializers.ValidationError("you are trying to assign duty to someone that is not in your organization!")

        return data

    class Meta:
        model = models.duty
        fields = ('id','owner','persons','title','duty_description','date_posted','deadline','organization')
        extra_kwargs = {'owner': {'read_only': True}}

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model =models.Organization
        fields = ('id','name','description')