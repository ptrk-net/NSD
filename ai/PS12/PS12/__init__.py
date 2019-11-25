from gym.envs.registration import register

register(
    id='ps12-v0',
    entry_point='PS12.envs:ps12Env'
)