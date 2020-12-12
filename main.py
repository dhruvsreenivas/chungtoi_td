from game import ChungToi
from models import Agent

game = ChungToi()
agent = Agent(td_lam=0.7, lr=0.0012, eps=0.85)
adversary_agent = Agent(td_lam=0.7, lr=0.0012, eps=0.15)
