import json

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt

from words import saveNewWord, getRandomWord, getWords

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
    word_info = getRandomWord()
    return HttpResponse(json.dumps(word_info), content_type="application/json")

def getWordCount(request):
    username = request.session['username']
    count = Word.objects.filter(user_id=username).count()
    return count

@csrf_exempt
def getWordsByOffset(request):
    offset = request.GET.get('offset')
    username = request.session['username']
    result = getWords(6, int(offset), username)
    return HttpResponse(json.dumps(result), content_type="application/json")