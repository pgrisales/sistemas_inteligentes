from agent import Agent
from game import Game
from rules import rules
from browser import Browser
from capture import agent_pos
from solver import solver


def run(agent: Agent, move, game: Game):
  game.state = rules(agent, move, game)
  return game.state

class Env:
  def __init__(self, level):
    self.level = level

# Level 0: (5,2)
  def test(self):
    a_pos = (5,2)
#    browser = Browser(self.level)
#    a_pos = agent_pos(browser.get_board())
    agent = Agent(a_pos)
    game = Game(self.level-1, a_pos)

    solver(game, agent)
#    ps = game.possible_actions(agent, game)
#    print(agent.pos)
#    for k, v in ps.items():
#      print(v())
    i = 1
#    while not game.finish:
#      print(run(agent, agent.testRules(), game))
#      print('Possible desicions: ', len(game.possible_actions(agent,game)))
#      print('##### ', len(game.diamonds) , ' ####')
#      print('##### ', agent.pos , ' ####')
#      print('##### Number of iterations: ', i, ' ####')
#      i += 1

  def start(self):
    #i = [5,2]
    i = [3, 3]
    tempL = 11
    agent = Agent(i)
    game = Game(tempL, i)
    i = 1
    while not game.finish:
      print(run(agent, game))
      print('##### ', len(game.diamonds) , ' ####')
      print('##### ', agent.pos , ' ####')
      print('##### ', i, ' ####')
      i += 1

#env = Env()
#env.start()
