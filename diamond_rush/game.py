
class Level:
### TODO: should count variables like diamonds?
  def __init__(self, level, a_pos):
    self.level = level
    # default init agent pos 
    self.a_pos = a_pos
    self.state, self.f_state = self.load_level(self.level, self.a_pos)
    self.p_state = self.state
    # remeber previous state
#    self.p_state = self.state

  def get_state(self):
    return self.state

  def get_f_state(self):
    return self.f_state

# TODO: define structure for previous and new state
  def new_state(self, agent: Agent):
    self.p_state, self.state = check_rules(agent, self.p_state, self.state)
    return self.state

  def load_level(self, level, a_pos): 
    #'./levels/1.png'
    level = level.split('/')
    level = level[2][:len(level[2])-4]

    state = np.loadtxt('./levels/default_init_states/' + level,dtype=str)
    f_state = np.loadtxt('./levels/final_states/' + level,dtype=str)

    if a_pos != self.agent_pos(state):
      # TODO: update new state with agent new position
      new_state = state
      return new_state, f_state

    return state, f_state

  def diamonds_pos(self, state):
    pos = []
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'd' or state[i,j] == 'D':
          pos.append((i,j))
    return pos 

  def agent_pos(self, state):
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'a' or state[i,j] == 'A' or state[i,j] == '@':
          return i,j
