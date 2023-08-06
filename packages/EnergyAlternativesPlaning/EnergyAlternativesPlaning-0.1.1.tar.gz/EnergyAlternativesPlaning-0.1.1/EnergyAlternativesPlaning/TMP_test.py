
#region importation of modules
import os
import sys
if sys.platform != 'win32':
    myhost = os.uname()[1]
else : myhost = ""
if (myhost=="jupyter-sop"):
    ## for https://jupyter-sop.mines-paristech.fr/ users, you need to
    #  (1) run the following in a terminal
    if (os.system(
            "/opt/mosek/9.2/tools/platform/linux64x86/bin/lmgrd -c /opt/mosek/9.2/tools/platform/linux64x86/bin/mosek.lic -l lmgrd.log") == 0):
        os.system("/opt/mosek/9.2/tools/platform/linux64x86/bin/lmutil lmstat -c 27007@127.0.0.1 -a")
    #  (2) definition of license
    os.environ["MOSEKLM_LICENSE_FILE"] = '@jupyter-sop'

#import docplex

from functions.f_model_definition import *
# Change this if you have other solvers obtained here
## https://ampl.com/products/solvers/open-source/
## for eduction this site provides also several professional solvers, that are more efficient than e.g. cbc
#endregion

#region Solver and data location definition
InputFolder='Data/input/'
solver= 'mosek' ## no need for solverpath with mosek.
BaseSolverPath='/Users/robin.girard/Documents/Code/Packages/solvers/ampl_macosx64'
sys.path.append(BaseSolverPath)

solvers= ['gurobi','knitro','cbc'] # 'glpk' is too slow 'cplex' and 'xpress' do not work
solverpath= {}
for solver in solvers : solverpath[solver]=BaseSolverPath+'/'+solver
cplexPATH='/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx'
sys.path.append(cplexPATH)
solverpath['cplex']=cplexPATH+"/"+"cplex"
solver = 'mosek'
#endregion

#region VI Ramp+Storage Multi area : loading parameters
Zones="FR_DE_GB_ES"
year=2016
Selected_AREAS=["FR","DE"]
Selected_TECHNOLOGIES=['OldNuke', 'CCG','WindOnShore',"curtailment"] #you'll add 'Solar' after #'NewNuke', 'HydroRiver', 'HydroReservoir','WindOnShore', 'WindOffShore', 'Solar', 'Curtailement'}

#### reading CSV files
TechParameters = pd.read_csv(InputFolder+'Planing_MultiNode_DE-FR_TECHNOLOGIES_AREAS.csv',
                             sep=',',decimal='.',comment="#").set_index(["AREAS","TECHNOLOGIES"])
areaConsumption = pd.read_csv(InputFolder+'areaConsumption'+str(year)+'_'+str(Zones)+'.csv',
                                sep=',',decimal='.',skiprows=0,parse_dates=['Date']).set_index(["AREAS","Date"])
availabilityFactor = pd.read_csv(InputFolder+'availabilityFactor'+str(year)+'_'+str(Zones)+'.csv',
                                sep=',',decimal='.',skiprows=0,parse_dates=['Date']).set_index(["AREAS","Date","TECHNOLOGIES"])

ExchangeParameters = pd.read_csv(InputFolder+'Hypothese_DE-FR_AREAS_AREAS.csv',
                                 sep=',',decimal='.',skiprows=0,comment="#").set_index(["AREAS","AREAS.1"])
StorageParameters = pd.read_csv(InputFolder+'Planing_MultiNode_AREAS_DE-FR_STOCK_TECHNO.csv',sep=',',decimal='.',comment="#",skiprows=0).set_index(["AREAS","STOCK_TECHNO"])

#### Selection of subset
TechParameters=TechParameters.loc[(Selected_AREAS,Selected_TECHNOLOGIES),:]
areaConsumption=areaConsumption.loc[(Selected_AREAS,slice(None)),:]
availabilityFactor=availabilityFactor.loc[(Selected_AREAS,slice(None),Selected_TECHNOLOGIES),:]
TechParameters.loc[(slice(None),'CCG'),'energyCost']=300 ## margin to make everything work
TechParameters.loc[(slice(None),"OldNuke"),'RampConstraintMoins']=0.01 ## a bit strong to put in light the effect
TechParameters.loc[(slice(None),"OldNuke"),'RampConstraintPlus']=0.02 ## a bit strong to put in light the effect
#endregion

Parameters={"areaConsumption"      :   areaConsumption,
                                                   "availabilityFactor"   :   availabilityFactor,
                                                   "TechParameters"       :   TechParameters,
                                                   "StorageParameters"   : StorageParameters,
                                                   "ExchangeParameters" : ExchangeParameters}

model = Create_pyomo_model_sets_parameters(Parameters)  # areaConsumption, availabilityFactor, TechParameters)
model = set_Operation_base_variables(model)  # energy energyCosts  if AREAS --> exchange if storage...
model = set_Operation_flex_variables(model)
model = set_Planing_base_variables(model)  # defined variables :  capacityCosts capacity
model = set_Planing_flex_variables(model)


import re# sys
EQs={}
EQs["energyCtr" ] =    {
        "domain"   : ["AREAS","Date"],
        "equation" : "sum(energy|TECHNOLOGIES) +sum(exchange|AREAS) + sum(storageOut+storageIn|STOCK_TECHNO) == areaConsumption"}

EQ =    { "name" : "energyCtr",
        "domain"   : ["AREAS","Date"],
        "equation" : "sum(energy|TECHNOLOGIES) +sum(exchange|AREAS) + sum(storageOut+storageIn|STOCK_TECHNO) == areaConsumption"}


def math_to_pyomo_constraint(EQs,model,verbose =False):
    Set_names = get_allSetsnames(model)
    Parameters_names = get_ParametersNameWithSet(model)
    Variables_names = get_VariableNameWithSet(model)

    for curConstraintName in EQs.keys():
        EQ = EQs[curConstraintName];
        EQ["name"]= curConstraintName
        for param in Parameters_names:
            SET_val_names=[name+"_val" for name in Parameters_names[param]]
            EQ["equation"]=EQ["equation"].replace(param,"model."+param+"["+",".join(SET_val_names)+"]")

        for variable in Variables_names:
            SET_val_names=[name+"_val" for name in Variables_names[variable]]
            EQ["equation"]=EQ["equation"].replace(variable,"model."+variable+"["+",".join(SET_val_names)+"]")

        for SET in Set_names:
            SET_val_names=[name+"_val" for name in Variables_names[variable]]
            EQ["equation"]=EQ["equation"].replace("|"+SET," for "+SET+"_val"+" in model."+SET)

        regexp = re.compile("sum\([^\)]* for AREAS_val in model.AREAS\)")
        searched = regexp.search(EQ["equation"])
        if bool(searched):
            replacement = regexp.search(EQ["equation"])[0].replace("AREAS_val,AREAS_val","b,AREAS_val")
            replacement= replacement.replace("for AREAS_val in model.AREAS","for b in model.AREAS")
        EQ["equation"] = regexp.sub(replacement,EQ["equation"])

        EQ["equation"]

        domain_name = [name+"_val" for name in EQ["domain"]]
        Constraint_function_definition = "def "+EQ["name"]+"_rule(model,"+",".join(domain_name)+"):\n"+"\t return "+EQ["equation"]
        if verbose: print(Constraint_function_definition)
        exec(Constraint_function_definition)
        domain_model = ["model."+name for name in EQ["domain"]]
        Constraint_assignation = "model."+EQ["name"]+"=Constraint("+",".join(domain_model)+",rule="+EQ["name"]+"_rule)"
        if verbose: print(Constraint_assignation)
        exec(Constraint_assignation)
    return model


def math_to_pyomo_constraint(Vars, model, verbose=False):
    Set_names = get_allSetsnames(model)
    Parameters_names = get_ParametersNameWithSet(model)
    Variables_names = get_VariableNameWithSet(model)

    for curVarName in Vars:

        Var_definition_script_splitted = re.compile("[\[\]]").split(curVarName)
        for SET in Set_names:
            Var_definition_script_splitted[1] = Var_definition_script_splitted[1].replace(SET, "model." + SET)
        Domain_text = Var_definition_script_splitted[2]
        if Domain_text=="":
                Var_Domain = ""
        elif Domain_text == ">=0":
                Var_Domain = ",domain=NonNegativeReals"
        elif Domain_text=="<=0":
                Var_Domain = ",domain=NonPositiveReals"
        elif bool(re.compile(Domain_text).search("(.+)\-(.+)")):
                domain_split = re.compile(Domain_text).split("\-")
                Var_Domain = ",bounds=(" + domain_split[0] + "," + domain_split[1] + ")"

        Var_definition_script = "model." + Var_definition_script_splitted[0] + "=Var(" + Var_definition_script_splitted[
            1] + Var_Domain + ")"

        exec(Var_definition_script)