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
    def post(self, request, **kwargs):
        player_A = request.POST.get('playerA')
        player_B = request.POST.get('playerB')
        match_result = request.POST.get('match_result')
        # Process the above data and store in .txt and update .json

        f = open('results.txt', 'a')
        f.write(player_A + ',' + player_B + '\n')  # python will convert \n to os.linesep
        f.close()

        env = TrueSkill(draw_probability=0)
        players = ['Henry','Ryan','Ben','Kieran','Guyon','Kahloon']
        ratings = {player:Rating() for player in players}
        matches = [r.split(',') for r in open("results.txt", "r").read().split('\n')[:-1]]
        for [winner,loser] in matches:
            (ratings[winner],ratings[loser]) = rate_1vs1(ratings[winner], ratings[loser], drawn=False, min_delta=0.0001, env=env)
        leaderboard = sorted(players, reverse=True, key=lambda x : ratings[x].mu)
        data = {'leaders':[],'maxScore':50}
        for i,p in enumerate(leaderboard):
            data['leaders'].append({'id':i+1,'name':p,'score':ratings[p].mu})
        with open('data.json', 'w') as fp:
            json.dump(data, fp)

        return redirect('/')

    def get(self, request, **kwargs):
        return redirect('/')


class JsonServerView(TemplateView):
    def get(self, request, **kwargs):
        with open('data.json','r') as json_data:
            return JsonResponse(json.load(json_data))
