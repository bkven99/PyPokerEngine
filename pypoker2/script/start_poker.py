# HOW TO USE
# python pypoker2/script/start_poker.py --config_path /Users/kota/development/PyPoker2/pypoker2/script/config.json

# Resolve path configucation
import os
import sys
import importlib
import argparse
import json

root = os.path.join(os.path.dirname(__file__), "..", "..")
src_path = os.path.join(root, "pypoker2")
sys.path.append(root)
sys.path.append(src_path)

# Start script code from here
from pypoker2.interface.dealer import Dealer
from pypoker2.players.sample.fold_man import PokerPlayer as FoldMan

def parse_args():
  parser = argparse.ArgumentParser(description="Receive path of config file")
  parser.add_argument("--config_path", help="absolute path to config.json file")
  args = parser.parse_args()
  return args.config_path

def read_config(config_file_path):
  with open(config_file_path) as f:
    return json.load(f)

def setup_players_info(config):
  return [read_player_info(json_info) for json_info in config["players_info"]]

def read_player_info(json_info):
  name = json_info["name"]
  algorithm = read_algorithm(json_info["algorithm_path"])
  return { "name": name, "algorithm": algorithm }

def read_algorithm(algo_path):
  sys.path.append(os.path.dirname(algo_path))
  algo_file_name = os.path.basename(algo_path)
  m = importlib.import_module(os.path.splitext(algo_file_name)[0])
  try:
    return m.PokerPlayer()
  except AttributeError as e:
    raise NotImplementedError("PokerPlayer class is not found in [{0}]" % algo_path)

def play_game(config, players_info):
  dealer = Dealer(config["small_blind_amount"], config["initial_stack"])
  for info in players_info:
    dealer.register_player(info["name"], info["algorithm"])
  return dealer.start_game(config["max_round_count"])

def main():
  config_file_path = parse_args()
  config = read_config(config_file_path)
  players_info = setup_players_info(config)
  result = play_game(config, players_info)
  print result

if __name__ == '__main__':
  main()
