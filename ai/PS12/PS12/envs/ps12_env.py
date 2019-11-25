import gym
from gym import error, spaces, utils
from gym.utils import seeding

class ps12Env(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, log_level, db_server, db_port, counters, sync_queue):
    self.log_level = log_level
    self.db_server = db_server
    self.db_port = db_port

  def step(self, action):
    raise NotImplementedError('Working...')

  def reset(self):
    raise NotImplementedError('Working...')

  def render(self, mode='human', close=False):
    raise NotImplementedError('Working...')

