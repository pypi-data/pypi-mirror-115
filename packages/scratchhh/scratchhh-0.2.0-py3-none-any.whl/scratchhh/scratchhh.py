import requests
import json
import bs4
import os
import re

os.chdir(os.getcwd())

class Scratch:
    API_URL = 'https://api.scratch.mit.edu/'
    CDN_URL = 'https://cdn2.scratch.mit.edu/'

    def getUserProj(user:str, num=1):
        r = json.loads(requests.get('{}users/{}/projects/'.format(Scratch.API_URL, user)).text)
        ids = []
        for i in range(0, num):
            ids.append(str(r[i]['id']))
        return ids

    def getThumb(id:str, file='thumbnail.png'):
        r = requests.get('{}get_image/project/{}_640x372.png'.format(Scratch.CDN_URL, id), stream=True)
        if r.status_code == 200:
            with open(file, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        else:
            print('The ID for this project is invalid!')

    def searchProj(query:str, num=1):
        r = json.loads(requests.get('{}search/projects/?mode=trending&q={}'.format(Scratch.API_URL, query)).text)
        ids = []
        for i in range(0, num):
            ids.append(str(r[i]['id']))
        return ids

    def getInfo(id:str):
        r = json.loads(requests.get('{}projects/{}'.format(Scratch.API_URL, id)).text)
        j = { 'title':r['title'],'author':r['author']['username'],'share':r['history']['shared'],'stats':r['stats'] }
        return j

    def getUserAv(user:str, file='userav.png'):
        r = requests.get(json.loads(requests.get('{}users/{}'.format(Scratch.API_URL, user)).text)['profile']['images']['90x90'])
        if r.status_code == 200:
            with open(file, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        else:
            print('The given username is invalid!')

    def exists(ini:str):
        if re.match('^[0-9]*$', ini):
            r = requests.get('https://api.scratch.mit.edu/projects/{}'.format(ini))
            if r.status_code == 200:
                return True
            else:
                return None
        elif re.match('^[a-zA-Z]+$', ini, re.IGNORECASE):
            r = requests.get('https://api.scratch.mit.edu/users/{}'.format(ini))
            if r.status_code == 200:
                return True
            else:
                return None

    def getProjComments(id:str, num=1):
        r = requests.get('https://scratch.mit.edu/site-api/comments/project/{}/'.format(id))
        soup = bs4.BeautifulSoup(r.text, 'html.parser')

        rawcomments = []
        formattedcomments = []

        for tr in soup.find_all('li'):
            values = [div.text.strip('\n') for div in tr.find_all('div', {'class':'comment'})]
            rawcomments.append(values)

        def Commentformat(string):
            comment = string.replace('        ', '').replace('\n\n', '').replace('Reply', '').replace('    ', '').split('\n')
            while '  ' in comment:
                comment.remove('  ')
            return comment

        for i in range(0, num):
            comment = rawcomments[i][0]
            formattedcomments.append(Commentformat(comment))
        
        return formattedcomments
            