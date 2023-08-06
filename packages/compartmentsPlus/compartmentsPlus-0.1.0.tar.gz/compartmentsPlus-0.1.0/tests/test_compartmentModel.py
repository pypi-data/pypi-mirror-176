from ..compartmentModel import compartmentModel
import pytest

#TODO: decide how to test internal methods
#def __init__(self, tmax=0, compartments=[], parameters=[], linkages={}, initCompartments={}, initParameters={}, parameterPoints=[]):
#def _generate_model(self):
#def _generate_compartment_list(self):
#def _generate_parameters_list(self): #Adds all parameters to parameters list and updates all parameters that have change points
#def _update_parameter(self, name:str): #Given parameter list and change point tuple, update all points necessary in parameter list      
#def _evalLink(self, time:int, key):
#def _stepEval(self, time:int, verbose=False):


#def add_compartment(self, name:str, initVal):
#Basic outcome
def test_add_compartment_base():
    errors = []
    expectedInitCompartments = {'A': 10, 'B':1}
    expectedCompartments = [{'A': 10, 'B':1},{'A': 10, 'B':1},{'A': 10, 'B':1},{'A': 10, 'B':1},{'A': 10, 'B':1}]

    temp = compartmentModel(tmax=5)
    temp.add_compartment('A', 10)
    temp.add_compartment('B', 1)

    if not temp.initCompartments == expectedInitCompartments:
        errors.append('Error generating initCompartments dict.')
    if not temp.compartments == expectedCompartments:
        errors.append('Error generating compartments list')

    del temp
    assert not errors, "errors occured:\n{}".format("\n".join(errors))
#Compartment already exists
def test_add_compartment_failure():
    temp = compartmentModel(tmax=5)
    try:
        temp.add_compartment('A', 10)
        temp.add_compartment('A', 5)
    except Exception as err:
        print(err)
        del temp
        assert str(err) == "Model Generation Error: compartment name (A) already in use"

#def del_compartment(self, name:str):
#Basic outcome
def test_del_compartment_base():
    errors = []
    expectedInitCompartments = {'A': 10}
    expectedCompartments = [{'A': 10},{'A': 10},{'A': 10},{'A': 10},{'A': 10}]

    temp = compartmentModel(tmax=5)
    temp.add_compartment('A', 10)
    temp.add_compartment('B', 1)
    temp.del_compartment('B')

    if not temp.initCompartments == expectedInitCompartments:
        errors.append('Error generating initCompartments dict.')
    if not temp.compartments == expectedCompartments:
        errors.append('Error generating compartments list')

    assert not errors, "errors occured:\n{}".format("\n".join(errors))
#Compartment doesn't exist


#def edit_compartment(self, name:str, initVal):
#def sum_compartments(self, t:int, names:list):
#def add_parameter(self, name:str, initVal):
#def edit_parameter(self, name:str, initVal):
#def del_parameter(self, name:str):    #Deletes parameter from initParameters and all change points associated with it
#def add_parameter_change(self, name:str, newVal, timeStart:int):    #Adds parameter change point and updates parameters if name matches existing parameter. If change already exists at time point, its replaced
#def del_parameter_change(self, name:str, timeStart:int):    #Removes parameter change point at time point if exists
#def del_all_parameter_changes(self, name:str):    #Removes all parameter changes for single parameter if name matches existing parameter
#def reset_parameters(self):    #Removes all changes for all parameters and resets to init values
#def add_linkage(self, fromCompartment:str, toCompartment:str, changeFunction:str):
#def del_linkage(self, fromCompartment:str, toCompartment:str):
#def edit_linkage(self, fromCompartment:str, toCompartment:str, changeFunction:str):
#def run(self, verbose = False):
#def get_tmax(self):
#def get_all_compartments(self):
#def get_initCompartments(self):
#def get_compartment(self, name:str):
#def get_initParameters(self):
#def get_all_parameters(self):
#def get_parameter(self, name:str):
#def get_parameter_changes(self):
#def get_linkages(self):
#def get_comparison_data(self):
#def get_compartment_names(self):
#def get_parameter_names(self):
#def get_dates_for_parameter(self, parameter):
#def get_linkage_names(self):
#def get_initCompartments_df(self):
#def get_parameterValues_df(self):
#def get_linkage_df(self):
#def get_compartments_df(self):
#def set_compartments(self, compartmentMatrix):
#def set_initCompartments(self, compartmentDict):
#def set_initParameters(self, parametersDict):
#def set_all_parameters(self, parametersMatrix):
#def set_parameter(self, name:str, parameterList):
#def set_parameter_changes(self, changeList):
#def set_linkages(self, linkageDict):
#def create_json(self):
#def write_json(self, fileName='model.json', filepath=''):
#def load_from_json(self, jsonFile=None, jsonObject=None):
#def write_compartments_to_csv(self, filename='model.csv', filepath=''):
#def extract_columns(self, csvList):
#def import_comparison_data(self, filepath):
#def MAE(self, predicted, observed):
#def MAE_overtime(self, predicted, observed):
#def MAPE(self, predicted, observed):
#def MAPE_overtime(self, predicted, observed):
#def MSE(self, predicted, observed):
#def MSE_overtime(self, predicted, observed):
#def RMSE(self, predicted, observed):
#def RMSE_overtime(self, predicted, observed):
#def NRMSE(self, predicted, observed):
#def NRMSE_overtime(self, predicted, observed):
#def plot_model(self, nameList): #Plots models based on name of item, this requires that your model and import data have unique names
#def genetic_algorithm(self, predicted, observed, numGenerations, numChromosomes, mutationChance):
#def generate_random_chromosome(self, genePercent = 0.20):
#def randParamValue(self, parameter, variance=5):
#def randParamDate(self):
#def fitness_func(self, predicted, observed):
#def population_selection(self, population, predicted, observed):
#def crossover_func(self, chrom1, chrom2):
#def mutate_chromosome(self, chromosome):