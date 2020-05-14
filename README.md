# Organization project
> organize your duties


the purpose of this project is to organize and share duties among the Managers and partners of companies.
by using this project you can easily see the assignments that assigned to you, 
and also you are ableto follow up the assignment that you declare for your workers.


## prerequisites
 before using this project you should install the version of python that you want.
if you going to use default configuration of this project you should make postgress database in your system
and change the setting.py to be compatible with that database!
## Installation

#### installing django:

```sh
 python -m pip install Django
```
#### installing Django rest framework
```sh
pip install djangorestframework
```
download project and by opening the shell in project directory, run this commands :
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```
```sh
python manage.py runserver
```
now you are ready to use api!
## the model and database

I used 4 table and entity to do this project. you can see theme and theire realtions in this picture:

![](http://www.mediafire.com/convkey/341d/kfb62gda2uew1wzzg.jpg?size_id=6)

#### duty
each duty has many to many field,named persons and that means this duty assigned to these persons.the duty has owner field too and this field is the id of somebody that make this duty.there is also organization field in duty that show this duty is for each organization.

#### UserProfile
every user in system authenticate in login page with email and its password. after authentication the api return some random Token in response. then we should put this Token in header as Authentication and then we can access all the functions that is made for our roll.
the roll field could be Admin,Worker,Org_worker and Manager. when you fisrt make User Profile you should put roll to Worker and organization field to None otherwise the system rise an error.

#### Request
we have 3 type of request in system: worker_to_org_worker, worker_to_manager and org_worker_to_manager.
instead of declaring table for each request, i used some field to seprate these request.
for exampe if we want to build worker_to_manager request we set from_user to worker that make this request and then put job_title of request to Manager and these request should go for admins, so we put to_see field to Admin.

#### Organization
this table is so simple and has name of organization and some descriptions about this organization.


## testing some senarios:
I suppouse that you successfully make migrations and configure your data base to our project and then migrate all objects.
now its time for do some test.
before we begin test, make sure that you install modHeader plugin for google chrom. this plugin will use to put some Token into our request to api.for example if we are manager and we want to do our staff we should login and this give us some Token. then open modHeader and type Authorization in left field then in right field type Token and then paste your Token that api gave to you. after that you consider the authorizied user and can do the works you are alow to do as manager.
if you uncheck the row in modHeader it does not put that Token in header and this means you are logged out.
in shell go to project directory and type
```sh
python manage.py runserver
```
### sign up
then you can use api from 127.0.0.1 or localhost.<br>
for using api you should first make an account. for doing this go to this url:<br>
[http://127.0.0.1:8000/profile/](http://127.0.0.1:8000/profile/)
make some user with some fake information. as you can see if you dont put roll to worker the server give you response and user wil not created.<br>
we have no organization yet, but if you try to declare organization in this step, it will raise error again.<br>
I will call this worker testUser1 in future<br>
if you are admin user and want to sign up,type this command in the root of project:<br>
```sh
python manage.py createsuperuser
```
this command ask you the information of your account and then create admin account for you.<br>
I will call this user adminUser in future.
### login
now we want to login as adminUser and then create some organization. for doing this go to this addres:
[http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)<br>
and then enter the email and password of adminUser.the api gives you some Token. put this token in modHeader and make sure you are checked with this Token.<br>
now you are signed in as admin and you can make organization. for doing this go to this address:
[http://127.0.0.1:8000/organization](http://127.0.0.1:8000/organization/)<br>
this address mapped to the ModelView set that only admin has permission to see and alter. as you can see you can make organization and also you can delete,put and path each organization by using this adress:
http://127.0.0.1:8000/organization/<organization_id>/<br>
make two organization with these names : org1 and org2 or any other name that you want.

### worker_to_manager request
now its time to testUser1 request to become Manager of org1.for doing this first login with testUser1 account (go to login and then copy token to modHeader). after logging in go to this address:<br>
[http://127.0.0.1:8000/worker_to_manager_req/](http://127.0.0.1:8000/worker_to_manager_req/)<br>
it is modelViewSet that you can make worker to Manager request, if you are worker and you can also edite and delete your worker to manager requests by putting the id of request after this url.<br>
if you put from_user to somebody that is not you, its raise an error and say you should request for your self. make two request, one for manager of org1 and one for manager of org2. then logout buy uncheking the testUser1 in modHeader and check the check box related to adminUser and go to this address again.<br>
if you are admin in worker_to_manager_req you should see all the requests that came from all workers to become manager of some organization. the admin can just see these request and it can not be changed by admin. we make to request, so the admin should see this 2 requests. now suppouse that admin find out that you are realy manager of org1 and he want to accept the request that is related to org1.he pick the id of request(it is 1 for me) and make get request to this address:<br>
[http://127.0.0.1:8000/accept/1](http://127.0.0.1:8000/accept/1)<br>
you can also reject request by calling this url by get method and put id of request after this address:<br>
[http://127.0.0.1:8000/reject/1](http://127.0.0.1:8000/reject/1)<br>
accepting worker to manager request cause that all the requests that came from the user that make this request, will be deleted.
but rejecting worker to manager request dont alter another requests of this user.
so accept the request of testUser1 that related to org1. now the roll of testUser1 should be changed to "MG" (manager).
you can check it by calling the /profile/ address. if you are admin this url, will show all the informations of all users.
but if you are manager calling /profile/ show you all the informations of your organization worker and if you are org_worker or worker calling /profile/ will give you the information that only related to ypu.

### worker_to_org_worker request
now its time to make organization worker, that works in org1 company.(company that its manager is testUser1).
as I explained above,log out and then make another worker user, that his name is testUser2.
now this test User want to be the org_worker of org1. for making request go to this address as worker:<br>
[http://127.0.0.1:8000/worker_to_orgworker_req/](http://127.0.0.1:8000/worker_to_orgworker_req/)<br>
make your request for org1 (this is similar to making worker to Manager). you can also edit your request by putting the id of request after this url.
now log out and go to testUser1 account.(the admin cant see this request. only manager can see) go to this address again. now you should see the request came from testUser2 for org_worker of your company.
for accepting this request, similar to accepting worker_to_manager request, pick id of request and use /accept/id_of_req (like before) you can also reject request by /reject/id_of_req.<br>
so accept the request and then testUser2 become the org_worker if org1 and testUser1 is manager of org1.

### org_worker_to_manager request
its similar to last 2 request. you should sign in as org_worker so you can make request in this url:<br>

[http://127.0.0.1:8000/orgworker_to_manager_req/](http://127.0.0.1:8000/orgworker_to_manager_req/)<br>

and then sign in as manager and you can see all the org_worker_to_manager that is related to your company.you can accept each request by /accept/requestId
if you are interesting you can test this. but it is a litle redundancy in this read me to make another manager in this way.
so until this point we have testUser1 and testUser2, first is manager and second in org_worker of one company.

### duty
now we sign in as testUser1 and go to this adress:<br>
[http://127.0.0.1:8000/duty/](http://127.0.0.1:8000/duty/)<br>
this is modelViewSet for table duty. the owner of this duty will be you automaticly. select one or more persons that you want to assign this duty to theme. these person should be related to your organization, otherwise it rise an error. and also put organization field to the organization that you are manager of it,otherwise it rise an error.you cant also assign duty to your self.(because managers dont work!)<br>
in our senario we have just one user that we can assign our duty to him. so selet persons to testUser2 and organization to org1 and then make duty.you can see all the duties that you made by calling /duty/ with get. this will show all duties to you ordered buy deadline field. you can also edit your duties buy putting the id of duty at the end of url.
the admin can also change every duties that exist in data base buy putting the id after /duty/, but admin can not make duty.<br>
so sign in again as testUser2 and go to /duty/ adress. you can see all the duties that assigned to you.(including the duties that you assign to your self).
similar to Manager, org_worker can define duty, but in persons part this should only assign duty to yourself, otherwise it rise an error.



## the features that dont exist in senaio
the admin can change the roll of each user in system buy calling /profile/user_id and call put or patch.<br>
admins can also change the organization of user in similar manner.
you can alsp fire an org_worker. for doing this if you are admin, you can simply change the roll by patch method and this url: /profile/<org_worker_id> and if you are manager with method delete and /profile/<org_worker_id> you can fire a person that is in your organization.


## Meta

mohammad amin mirzaei – aminmirzaiee1374@gmail.com


