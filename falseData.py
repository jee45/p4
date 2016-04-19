print("false DATA!! ")


 #Used to make requests
"""
import requests
import string
from random import choice



def sequencedStringGenerator( letterSelector, repeats):
    string_val = "".join( string.ascii_lowercase[letterSelector:letterSelector+1] for i in range(repeats))
    return string_val



def randomStringGenerator(finalStringLength, thefirstNLettersOfTheAlphabet):
    string_val = "".join( choice(string.ascii_lowercase[:finalStringLength] + ' ') for i in range(thefirstNLettersOfTheAlphabet))
    return string_val



def makePosts(username, password, postToMake=None):
    session = requests.Session()
    response = requests.get('http://127.0.0.1:5000/')
    response = session.post('http://127.0.0.1:5000/login', data = {'username':username,'password':password})

    if response.url:
        if postToMake is None:
            for x in range(20):
                response = session.post('http://127.0.0.1:5000/submitNewPost', data = {'entry':str(x)})
        else:
            response = session.post('http://127.0.0.1:5000/submitNewPost', data = {'entry':str(postToMake)})


def createABunchOfUsers():
    for x in range(20):
        u = sequencedStringGenerator(x, 1)
        session = requests.Session()
        response = requests.get('http://127.0.0.1:5000/')

        response = requests.post('http://127.0.0.1:5000/createNewUser', data = {'username':u,
                                                                         'password':u,
                                                                         'confirm':u
                                                                         })

        response = requests.get('http://127.0.0.1:5000/logout')


#createABunchOfUsers()
"""