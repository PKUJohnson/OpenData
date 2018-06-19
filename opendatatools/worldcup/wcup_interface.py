# encoding: utf-8

from .wcup_agent import WorldCupAgent

wcup_agent = WorldCupAgent()

def load_data():
    return wcup_agent.load_data()

def set_proxies(proxies):
    return wcup_agent.set_proxies(proxies)

def get_champion_rank():
    return wcup_agent.get_champion_rank()

def get_finalgame_rank():
    return wcup_agent.get_finalgame_rank()

def get_wingame_rank():
    return wcup_agent.get_wingame_rank()

def get_game_rank():
    return wcup_agent.get_game_rank()

def get_year_rank():
    return wcup_agent.get_year_rank()

def get_champion_fistgame_stat():
    return wcup_agent.get_champion_fistgame_stat()

def get_goal_stat():
    return wcup_agent.get_goal_stat()

def get_champion_goal_stat():
    return wcup_agent.get_champion_goal_stat()