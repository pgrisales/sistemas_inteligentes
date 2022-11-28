class Agent:
  def __init__(self, agent_pos):
    self.pos = agent_pos 
    self.has_key = False
    self.count = 0
    self.actions = { 'l': self.left, 'r': self.right, 'u': self.up, 'd': self.down }
  
  def die(self):
    pass
    
  def compute(self):
    from random import randint
    i  = randint(0,3)
    d = ['l', 'r', 'u', 'd']
    if d[i] == 'l':
      return self.left()
    elif d[i] == 'r':
      return self.right()
    elif d[i] == 'u':
      return self.up()
    elif d[i] == 'd':
      return self.down()

  def play(self, state):
    #i, j = self.compute()
    while state[i, j] == 'w' or state[i, j] == 'l':
      i, j = self.compute()
    assert state[i,j] != 'w'
    assert state[i,j] != 'l'
    return i, j 

  def left(self):
    return [self.pos[0], self.pos[1] - 1]
  def right(self):
    return [self.pos[0], self.pos[1] + 1]
  def up(self):
    return [self.pos[0] - 1, self.pos[1]]
  def down(self):
    return [self.pos[0] + 1, self.pos[1]]