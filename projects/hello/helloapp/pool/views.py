# pool/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import redirect
import json
from trueskill import Rating, rate_1vs1, TrueSkill

# Create your views here.

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

class ProcessResultView(TemplateView):
    def get(self, request, **kwargs):
        player_A = request.POST.get('player_A')
        player_B = request.POST.get('player_B')
        match_result = request.POST.get('match_result')
        # Process the above data and store in .txt and update .json

        f = open('results', 'w')
        f.write(player_A + ',' + player_B + '\n')  # python will convert \n to os.linesep
        f.close()

        env = TrueSkill(draw_probability=0)
        players = ['henry','ryan','ben','kieran','guyon','kahloon']
        ratings = {player:Rating() for player in players}
        matches = [r.split(',') for r in open("results.txt", "r").read().split('\n')]
        for [winner,loser] in matches:
            (ratings[winner],ratings[loser]) = rate_1vs1(ratings[winner], ratings[loser], drawn=False, min_delta=0.0001, env=env)
        leaderboard = sorted(players, reverse=True, key=lambda x : ratings[x].mu)
        data = {'leaders':[],'maxScore':50}
        for i,p in enumerate(leaderboard):
            data['leaders'].append({'id':i+1,'name':p,'score':ratings[p].mu})
        with open('data.json', 'w') as fp:
            json.dump(data, fp)

        return redirect('/')

class JsonServerView(TemplateView):
    def get(self, request, **kwargs):
        json_data = json.load(data.json)
        return JsonResponse(json_data)
