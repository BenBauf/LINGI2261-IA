#!/usr/bin/env python3

import sys
import rpg
import minisat

# The first argument must reference a merchant file and the second argument must represent a level file
if len(sys.argv) < 2:
    print("Usage:", sys.argv[0], "MERCHANT_FILE LEVEL_FILE", file=sys.stderr)
    exit(1)

merchant = rpg.Merchant(sys.argv[1])
level = rpg.Level(sys.argv[2])
level_num_str = sys.argv[2].split("_")[1].split(".")[0]

clauses = []
# TODO
# Append all clauses needed to find the correct equipment in the 'clauses' list.
#
# Minisat variables are represented with integers. As such you should use
# the index attribute of classes Ability and Equipment from the rpg.py module
# 
# The equipments and abilities they provide read from the merchant file you passed
# as argument are contained in the variable 'merchant'.
# The enemies and abilities they require to be defeated read from the level file you
# passed as argument are contained in the variable 'level'
# 
# For example if you want to add the clauses equ1 or equ2 or ... or equN (i.e. a
# disjunction of all the equipment pieces the merchant proposes), you should write:
# 
clauses.append(tuple(equ.index for equ in merchant.equipments))

#abilities for equipments
for equ in merchant.equipments:
    for ab in equ.provides:
        clauses.append((2,[(0-equ.index,ab.index),(ab.index,)]))

#requires
requires=[]
for ab in level.abilities:
    requires.append(ab.index,)
clauses.append((len(level.abilities),requires))
    
#clauses.append()



# TOREPLACE should be the number of different variables present in your list 'clauses'
# 
# For example, if your clauses contain all the equipments proposed by merchant and
# all the abilities provided by these equipment, you would have:
TOREPLACE = len(merchant.abilities) + len(merchant.equipments)
#TOREPLACE = len(merchant.equipments)
sol = minisat.minisat(TOREPLACE, clauses)

equipment_sol = [eq for eq in sol if eq <= merchant.abi_base_index]

if equipment_sol is None:
    print("No solution")
else:
    print("Equipment needed to beat the level {:s}".format(level_num_str))
    for i in equipment_sol:
        if(i <= merchant.abi_base_index):
            print("  - " + (merchant[i].name))
    print("Total pieces of equipment needed: {:d}".format(len(equipment_sol)))
