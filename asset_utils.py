import json

CDRAGON_BASE_PATH = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/"

with open("lol_constants/cd_map-assets.json") as f:
  map_assets = json.load(f)

def get_game_icon_path(map_id, game_mode):
  map = next(map for map in map_assets[map_id] if map["gameMode"] == game_mode)

  return CDRAGON_BASE_PATH + map["assets"]["game-select-icon-active"].replace("lol-game-data/assets/", "").lower()

def get_parties_bg_path(map_id, game_mode):
  map = next(map for map in map_assets[map_id] if map["gameMode"] == game_mode)

  return CDRAGON_BASE_PATH + map["assets"]["parties-background"].replace("lol-game-data/assets/", "").lower()