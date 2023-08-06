__version__ = '0.1.0'
from gym.envs.registration import register

register(
    id='causalenv-v0',
    entry_point='gym_causalenv.envs:CausalEnv',
)