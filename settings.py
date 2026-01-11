# settings.py
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

# Offset for hitboxes to create depth
HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'mirage': -10,
	'invisible': 0,
    'cloud': 0} 

# Biome Thresholds (Y-coordinates)
ZONE_THRESHOLDS = {
    'mangrove': 4000, 
    'winter': 2000    
}

# Knowledge Unlock Requirements
UNLOCK_REQUIREMENTS = {
    'mangrove': 30, 
    'winter': 60    
}

# UI Settings
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# Colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# Weapon Data
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'../graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'../graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../graphics/weapons/sai/full.png'}}
	# settings.py - Add this to the weapon_data
weapon_data = {
	'sword':  {'cooldown': 100, 'damage': 15, 'graphic':'../graphics/weapons/sword/full.png', 'cost': 0},
	'lance':  {'cooldown': 400, 'damage': 30, 'graphic':'../graphics/weapons/lance/full.png', 'cost': 100},
	'axe':    {'cooldown': 300, 'damage': 20, 'graphic':'../graphics/weapons/axe/full.png', 'cost': 150},
	'rapier': {'cooldown': 50,  'damage': 8,  'graphic':'../graphics/weapons/rapier/full.png', 'cost': 200},
	'sai':    {'cooldown': 80,  'damage': 10, 'graphic':'../graphics/weapons/sai/full.png', 'cost': 250}}

# Add this to monster_data to reward the player with money (exp will act as currency)
# In this version, we will use 'exp' as the currency for the shop.

# Magic Data
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'../graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'../graphics/particles/heal/heal.png'}}

# Monster Data (Renamed raccoon to ringtail)
monster_data = {
	'squid': {'health': 150,'exp':100,'damage':25,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'ringtail': {'health': 400,'exp':250,'damage':50,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 120,'exp':110,'damage':15,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 100,'exp':120,'damage':12,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}