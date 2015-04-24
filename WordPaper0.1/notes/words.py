import json

from notes.models import Word


def saveNewWord(origin, mean, explanation, username):
  """
    save the new word to DB, if it already exists, add its count and level
    @type origin: string
    @param origin: the origin word
    @type mean: string
    @param mean: the mean of the word
    @type explanation: string 
    @param explanation: the detail explanation of the word
    @type username: string
    @param username: the username of the creator
    @rtype: boolean
    @return whether this word already exists
    """
  try:
    word_obj = Word.objects.get(origin_word=origin)
    word_obj.count = word_obj.count + 1
    word_obj.level = calWordLevel(word_obj)
    word_obj.save()
    return False
  except:
    new_word = Word(origin_word=origin,
                    mean=mean,
                    explanation=explanation,
                    user_id=username,
                    level=0,
                    count=0)
    new_word.save()
    return True


def calWordLevel(word_obj):
  """
    calculate the level of word based on the count
    @type word_obj: Word
    @param word_obj: the Word object to be calculated
    @rtype: int
    @return the level for this word
    """
  current_count = word_obj.count
  new_level = current_count / 4
  return new_level

def getRandomWord():
    newWord = Word.objects.order_by('?')[0]
    result = {
        'origin': newWord.origin_word,
        'explanation' : newWord.explanation
    }
    return result

def getWords(count,offset, username):
    word_list = Word.objects.filter(user_id=username).order_by('id')[offset : offset+count]
    word_info_list = list()
    for word_obj in word_list:
        word_info = {
            'origin': word_obj.origin_word,
            'mean': word_obj.mean,
            'explanation': word_obj.explanation
        }
        word_info_list.append(word_info)
    result = {
        'words': word_info_list
    }
    return result