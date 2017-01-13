import os
from github import Github
from trello import TrelloApi

TRELLO_API_KEY = 'os.getenv("TRELLO_API_KEY")'
TRELLO_TOKEN = 'os.getenv("TRELLO_TOKEN")'
ICEBOX_ID = 'os.getenv("ICEBOX_ID")'
GITHUB_KEY = 'os.getenv("GITHUB_KEY")'

trello = TrelloApi(TRELLO_API_KEY, token=TRELLO_TOKEN)
g = Github("dianavermilya", GITHUB_KEY)

repos = ['IndicoApi', 'indico.io', 'Indico-FancyRouter', 'IndicoIo-Android',
         'IndicoIo-python', 'IndicoIo-R', 'IndicoIo-Java', 'IndicoIo-PHP',
         'IndicoIo-node', 'IndicoIo-ruby']

cards = {}
cardobjs = trello.lists.get_card_filter('open', ICEBOX_ID)
for cardobj in cardobjs:
    cards[cardobj['name']] = cardobj['id']

for repo in repos:
    for issue in g.get_repo('IndicoDataSolutions/' + repo).get_issues():
        if issue.title in cards:
            card = trello.cards.get(cards[issue.title])
            checklist = trello.cards.get_checklist(card['id'])
            if len(checklist) == 0:
                trello.cards.new_checklist(card['id'], None)
                trello.checklists.new_checkItem(card['id'], card['desc'])
                card['desc'] = None
            trello.checklists.new_checkItem(card['id'], issue.html_url)
        else:
            title = repo + ' #' + str(issue.number) + "\n" + issue.title
            card = trello.cards.new(title, ICEBOX_ID, desc=issue.html_url)
            cards[issue.title] = card['id']
