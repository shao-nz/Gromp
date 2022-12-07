import json

CDRAGON_BASE_PATH = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/"

with open("lol_constants/cd_map-assets.json") as f:
  map_assets = json.load(f)

with open("lol_constants/champion-summary.json") as f:
  champions_list = json.load(f)

def get_champion_portrait(champion_id):
  path = next(champ["squarePortraitPath"] for champ in champions_list if champ["id"] == champion_id)

  return CDRAGON_BASE_PATH + fix_asset_path(path)

def get_game_icon_path(map_id, game_mode):
  map = next(map for map in map_assets[map_id] if map["gameMode"] == game_mode)

  return CDRAGON_BASE_PATH + fix_asset_path(map["assets"]["game-select-icon-active"])

def get_parties_bg_path(map_id, game_mode):
  map = next(map for map in map_assets[map_id] if map["gameMode"] == game_mode)

  return CDRAGON_BASE_PATH + fix_asset_path(map["assets"]["parties-background"])

def fix_asset_path(path):
  return path.replace("lol-game-data/assets/", "").lower()