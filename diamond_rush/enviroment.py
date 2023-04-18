from agent import Agent
from game import Game
from rules import rules, possible_actions
from browser import Browser
from capture import agent_pos
from solver import solver, make_path

def run(agent: Agent, move, game: Game):
  a_pos = agent.pos
  key =  agent.has_key
  state = game.state
  diamonds = game.diamonds
  finish = game.finish
  level = game.level
  goal = game.g_pos
  pa = possible_actions(state, level, diamonds, finish, a_pos, key)
  game.state, d, game.finish, moved, agent.pos, k = rules(state, level, goal, diamonds, finish, a_pos, move, key)

  return game.state

class Env:
  def __init__(self, level):
    self.level = level

  def test(self):
    a_pos = (5,2)
    browser = Browser(self.level)
    a_pos = agent_pos(browser.get_board())
    agent = Agent(a_pos)
    game = Game(self.level-1, a_pos)

    moves = solver(game, agent)

    browser.move(moves)

  def start(self):
    i = [3, 3]
    tempL = 11
    agent = Agent(i)
    game = Game(tempL, i)
    i = 1
    while not game.finish:
      i += 1

