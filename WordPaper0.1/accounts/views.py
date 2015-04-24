import json
import hashlib

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User


def indexView(request):
    template = loader.get_template('accounts/index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


@csrf_exempt
def loginAction(request):
    """
    handle login request
    @type request: HttpRequest
    @param request: an object of HttpRequest which contains information
                    of HTTP request(FYI login information).
    @rtype: HttpResponsre
    @return an object of HttpResponse which contains a JSON array which 
            contains the verify result.
    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    result = {
        'isSuccessful': False,
        'isUsernameEmpty': not username,
        'isPasswordEmpty': not password,
        'isAccountValid': False
    }

    if not result['isUsernameEmpty'] and not result['isPasswordEmpty']:
        password = hashlib.md5(password).hexdigest()
        result['isAccountValid'] = isAccountValid(username, password)
        result['isSuccessful'] = result['isAccountValid']
        if result['isSuccessful']:
            createSession(request, username)

    return HttpResponse(json.dumps(result), content_type="application/json")


def isAccountValid(username, password):
    """
    verify the username and password
    @type username: string
    @param username: the username
    @type password: string
    @param password: the password for the username
    @rtype: boolean
    @return if the username and password for the user is valid
    """
    try:
        User.objects.get(Q(username=username), Q(password=password))
        return True
    except:
        return False


def createSession(request, username):
    """
    Create session for the user who just logded in
    @type request:HttpRequest
    @param request: the http request
    @type username:string
    @param usernmae: the username
    """
    request.session['isLoggedIn'] = True
    request.session['username'] = username


@csrf_exempt
def logoutAction(request):
    """
    User log out
    @type request:HttpRequest
    @param request: the http request
    @rtype: HttpResponseRedirect
    @return an object of HttpResponseRedirect which will redirect the user to the login page
    """
    try:
        del request.session['isLoggedIn']
        del request.session['username']
    except KeyError:
        pass

    return HttpResponseRedirect('/accounts/')


@csrf_exempt
def registerAction(request):
    """
    handler register request
    @type request: HttpRequest
    @param request: the HTTP request
    @rtype: HttpResponse
    @return an HttpResponse object that contains json which includes the register result
    """
    #get username and password
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    re_password = request.POST.get('repassword', '')
    # create result dict and check is password same
    result = {
        'isSuccessful': False,
        'isPasswordSame': password == re_password,
    }
    # check is user exists
    if result['isPasswordSame']:
        if not isUserExists(username):
            result['isSuccessful'] = True
            saveNewUser(username, password)
            createSession(request, username)
    return HttpResponse(json.dumps(result), content_type="application/json")


def isUserExists(username):
    try:
        User.objects.get(username=username)
        return True
    except:
        return False


def saveNewUser(username, password):
    password = hashlib.md5(password).hexdigest()
    new_user = User(username=username, password=password)
    new_user.save()
