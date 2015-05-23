import json

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt

from words import saveNewWord, getRandomWord, getWords, getMeanTest,setWordRemembered,increaseWordCount

from notes.models import Word

# Create your views here.


@csrf_exempt
def dashboardView(request):
    if not isUserLogin(request):
       return HttpResponseRedirect('/accounts/')
    template = loader.get_template('notes/note.html')
    context = RequestContext(request, {
        'count' : str(getWordCount(request))
    })
    return HttpResponse(template.render(context))

@csrf_exempt
def testView(request):
    if not isUserLogin(request):
       return HttpResponseRedirect('/accounts/')
    template = loader.get_template('notes/test.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

@csrf_exempt
def reviewView(request):
    if not isUserLogin(request):
       return HttpResponseRedirect('/accounts/')
    template = loader.get_template('notes/review.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

@csrf_exempt
def helpView(request):
    template = loader.get_template('notes/help.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def isUserLogin(request):
    try:
        isIn = request.session['isLoggedIn']
        return isIn
    except:
        return False


@csrf_exempt
def addWordAction(request):
    origin = request.POST.get('origin', '')
    mean = request.POST.get('mean', '')
    explanation = request.POST.get('explanation', '')
    username = request.session['username']
    isWordExists = not saveNewWord(origin, mean, explanation, username)
    result = {'isExists': isWordExists}
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getWordOfDay(request):
    username = request.session['username']
    word_info = getRandomWord(username)
    return HttpResponse(json.dumps(word_info), content_type="application/json")

@csrf_exempt
def getMeanTestWords(request):
    username = request.session['username']
    word_info = getMeanTest(username)
    return HttpResponse(json.dumps(word_info), content_type="application/json")

def getWordCount(request):
    username = request.session['username']
    count = Word.objects.filter(user_id=username).count()
    return count

@csrf_exempt
def wordRemembered(request):
    origin = request.GET.get('word')
    username = request.session['username']
    result = {
        'isSuccessful': setWordRemembered(origin, username)
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def increaseCountAction(request):
    origin = request.GET.get('word')
    print origin
    username = request.session['username']

    result = {
        'isSuccessful': increaseWordCount(origin, username)
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getWordsByOffset(request):
    offset = request.GET.get('offset')
    username = request.session['username']
    result = getWords(int(offset), username)
    return HttpResponse(json.dumps(result), content_type="application/json")