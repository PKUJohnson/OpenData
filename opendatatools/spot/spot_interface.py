# encoding: utf-8

from .spot_agent import SpotAgent

spot_agent = SpotAgent()

def get_commodity_spot_indicator():
    return spot_agent.get_commodity_spot_indicator()

def get_commodity_spot_indicator_data(indicator_id):
    return spot_agent.get_commodity_spot_indicator_data(indicator_id)

