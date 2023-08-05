import sys
from Create_game import create_game
from Validate_game import validate
from Shapley import Shapley
from CostGap import tauvalue
from Core import core_exists, is_in_core, least_core, minmax_core
from Nucleolus import nucleolus, nucl_screen
import pickle

GAMS_PATH=r'C:\GAMS\37\apifiles\Python'
sys.path.append(GAMS_PATH + r'\api_39')
sys.path.append(GAMS_PATH + r'\gams')
game_CHOSYN = pickle.load(open(r"C:\Users\Usuario\Documents\PhD Documents\Conferences\ESCAPE33\Models\GT Project\notebooks\CHOSYN_coal.p", "rb"))
#core_exists(game_CHOSYN, GAMS=True)
#print(minmax_core(game_CHOSYN, GAMS=True))
#print(least_core(game_CHOSYN, GAMS=True))
#print(nucleolus(game_CHOSYN, delta=0.9, GAMS=True))
import math
game_FULL = pickle.load(open(r"C:\Users\Usuario\Documents\PhD Documents\Conferences\ESCAPE33\Models\GT Project\notebooks\SIMPLE_coal.p", "rb"))
#game_FULL = pickle.load(open(r"C:\Users\Usuario\Documents\PhD Documents\Conferences\ESCAPE33\Models\GT Project\notebooks\FULL_coal.p", "rb"))
for ind in game_FULL.index:
    game_FULL['value'][ind] = math.ceil(game_FULL['value'][ind])
print(game_FULL)
#core_exists(game_FULL, GAMS=True)
#print(minmax_core(game_FULL, GAMS=True))
lcore = least_core(game_FULL, GAMS=True)
print(lcore)
print(is_in_core(game_FULL, lcore, eps=0.1))
shap = Shapley(game_FULL)
print(shap)
print(is_in_core(game_FULL, shap))
#print(nucleolus(game_CHOSYN, delta=0.9, GAMS=True))

'''game = create_game(5)
validate(game)
core_exists(game, GAMS=True)
tau = tauvalue(game)
print(is_in_core(game,tau))
print()
nucl = nucleolus(game, GAMS=True, delta=0.3)
print(is_in_core(game,nucl))
print()
print('\n:::::::INTERESTING STUF ::::::::\n')
lcore = least_core(game)
print(lcore)
mncore = least_core(game)
print(mncore)
shapley = Shapley(game)
print('Shapley:')
print(shapley)
print('\nNucleolus:')
print(nucl)
'''
