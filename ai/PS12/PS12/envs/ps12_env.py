import gym
from gym import error, spaces, utils
from gym.utils import seeding

class ps12Env(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, log_level, conversation, sync_queue):
    self.log_level = log_level
    self.conv = conversation
    self.sync_queue = sync_queue

    self.reward_range = (0, 100)
    self.action_space = spaces.Box(low=0, high=1, dtype=int)
    self.observation_space = spaces.Box(low=0, high=1)



  def step(self, action):
    raise NotImplementedError('Working...')

  def reset(self):
    raise NotImplementedError('Working...')

  def render(self, mode='human', close=False):
    raise NotImplementedError('Working...')

