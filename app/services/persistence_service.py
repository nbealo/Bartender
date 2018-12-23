import json,os,sys
from models.system_spec_model import SystemSpecModel
from models.ingredient_model import IngredientModel
from models.drink_model import DrinkModel
from models.drink_component_model import DrinkComponentModel

class PersistenceService:
    def __init__(self):
        pass
    
    @staticmethod
    def load_config(config_directory):
        spec = PersistenceService.load_system_spec(config_directory + '/system_spec.json')
        drinks = PersistenceService.load_drinks(config_directory + '/drinks')
        return (spec, drinks)

    @staticmethod
    def load_system_spec(json_path):
        try:
            spec = SystemSpecModel()
            with open(json_path) as f:
                data = json.load(f)
            spec.scale_pin_number = data['scale_pin_number']
            spec.scale_weight_offset = data['scale_weight_offset']
            spec.ingredients = []
            for ingredient_data in data['ingredients']:
                ingredient = IngredientModel()
                ingredient.name = ingredient_data['name']
                ingredient.volume = ingredient_data['volume']
                ingredient.pin_number = ingredient_data['pin_number']
                spec.ingredients.append(ingredient)
                
            return spec
        except KeyError as error:
            print('Bad spec configuration. ', error)
            raise error

    @staticmethod
    def load_drinks(drink_directory):
        files = os.listdir(drink_directory)
        drinks = []
        for file_name in files:
            file_path = drink_directory + '/' + file_name
            drink = PersistenceService.load_drink(file_path)
            drinks.append(drink)
        return drinks

    @staticmethod
    def load_drink(json_path):
        try:
            drink = DrinkModel()
            with open(json_path) as f:
                data = json.load(f)
                drink.name = data['name']
                drink.description = data['description']
                drink.components = []
                for component_data in data['components']:
                    component = DrinkComponentModel()
                    component.name = component_data['name']
                    component.volume = component_data['volume']
                    drink.components.append(component)
            return drink
        except KeyError as error:
            print('Bad drink configuration. ', error)
            raise error