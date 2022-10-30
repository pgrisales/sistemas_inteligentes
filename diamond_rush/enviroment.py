#!/usr/bin/env python3
from agent import Agent
from game import Game
from rules import rules

def run(agent: Agent, game: Game):
  game.state = rules(agent, game)
  return game.state

class Enviroment:

  def run(self):
    #i = [5,2]
    i = [3, 3]
    tempL = './levels/11.png'
    agent = Agent(i)
    game = Game(tempL, i)
#    print(game.state)
    i = 1
    while not game.finish:
      print(run(agent, game))
      print('##### ', len(game.diamonds) , ' ####')
      print('##### ', agent.pos , ' ####')
      print('##### ', i, ' ####')
      i += 1

env = Enviroment()
env.run()
