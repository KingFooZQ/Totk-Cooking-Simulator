import json
import os
import csv
import copy
import math
class TotkCookSim:
    LOCALE_PATH = r'locale/all_area_language.json'


    def __init__(self, area_lang='CNzh'):
        self.area_lang = area_lang
        self._load_data()


        pass

    def _load_data(self):
        with open('data/system_data.json', 'r') as jsonfile:
            self.system_data = json.load(jsonfile)

        with open('data/recipes.json', 'r', encoding='utf-8') as json_file:
            self.recipes = json.load(json_file)

        with open('data/roast_chilled_boiled.json', 'r', encoding='utf-8') as json_file:
            self.other_recipes = json.load(json_file)
        
        with open('data/recipe_card.json', 'r', encoding='utf-8') as json_file:
            self.recipe_card_table = json.load(json_file)

        self.material = {}
        with open('data/materials.json', 'r', encoding='utf-8') as json_file:
            materials = json.load(json_file)
            for item in materials:
                self.material[item['ActorName']] = item


        self.effect = {}
        with open('data/effects.json', 'r', encoding='utf-8') as json_file:
            effects = json.load(json_file)
            for item in effects:
                self.effect[item['EffectType']] = item

        self._index_material_name = {}
        with open(TotkCookSim.LOCALE_PATH, 'r', encoding='utf-8') as f:
            self._locale_dict = json.load(f)
            self._index_material_name_ = {}
            for key, value in self._locale_dict['Material'].items():
                if key.endswith('_Caption'):
                    continue
                for al in value.values():
                    if not al:
                        continue
                    self._index_material_name[al] = key.replace('_Name', '')

    def cook(self, materials, area_lang='CNzh') -> dict:
        self.area_lang = area_lang
        self._tmp = {}
        self._result = {}
        self.output = {}
        self._material(materials)
        self._recipe()
        self._hitpoint_recover()
        self._effect_type()
        self._effect_potency()
        self._effect_time()
        self._super_success_rate()
        self._selling_price()
        self._spice_boost()
        self._craft()
        self._locale()
        return self.output

    def _material(self, materials):
        materials_list = []
        for i in materials:
            actor_name = self._index_material_name[i]
            materials_list.append(self.material[actor_name])
        self._tmp['Materials'] = materials_list
        return

    def _recipe(self):
        materials_list = self._tmp['Materials']
        materials_name_tag = []
        for material in materials_list:
            actor_name = material['ActorName']
            cook_tag = material['CookTag']
            if (actor_name, cook_tag) not in materials_name_tag:
                materials_name_tag.append((actor_name, cook_tag))

        for recipe in self.recipes:
            m_copy = copy.copy(materials_name_tag)
            if recipe['ResultActorName'] == self.system_data['FailActorName']:
                self._tmp['Recipe'] = recipe
            recipe_str = recipe['Recipe']
            and_parts = recipe_str.split(' + ')
            parts_list = [i.split(' or ') for i in and_parts]
            if len(parts_list) > len(materials_name_tag):
                continue  

            all_ok = True
            for and_part in parts_list:
                and_ok = False
                for or_part in and_part:
                    for index in range(len(m_copy)):
                        material = m_copy[index]
                        if or_part == material[0] or or_part == material[1]:
                            m_copy.pop(index)
                            and_ok = True
                            break
                    if and_ok:
                        break
                if not and_ok:
                    all_ok = False
                    break
            if all_ok and recipe.get('IsSingleRecipe', False) == (len(materials_name_tag) == 1):
                self._tmp['Recipe'] = recipe
                return recipe

        return None
    
    def _hitpoint_recover(self):
        materials_list = self._tmp['Materials']
        hitpoint_recover = 0
        for material in materials_list:
            hitpoint_recover += material.get('HitPointRecover', 0)

        self._tmp['HitPointRecover'] = hitpoint_recover
        return

    def _effect_type(self):
        materials_list = self._tmp['Materials']   
        effect_list = []
        for material in materials_list:
            if material.get('CureEffectType') and material['CureEffectType'] not in effect_list:
                effect_list.append(material['CureEffectType'])
           
        if len(effect_list) == 1:
            self._tmp['Effect'] = self.effect[effect_list[0]]
        return
    
    def _effect_potency(self):
        materials_list = self._tmp['Materials']
        effect_potency = 0
        for material in materials_list:
            if material.get('CureEffectLevel'):
                effect_potency += material.get('CureEffectLevel', 0)

        self._tmp['EffectPotency'] = effect_potency
        return

    def _effect_time(self):
        effect = self._tmp.get('Effect')
        if not effect:
            self._tmp['EffectTime'] = 0
            return
        
        materials_list = self._tmp['Materials']
        effect_time = 0
        for material in materials_list:
            effect_time += material.get('CureEffectTime', 900) / 30
            if material.get('CureEffectType'):
                effect_time += effect.get('BaseTime', 0)
        self._tmp['EffectTime'] = effect_time
        return
    
    def _super_success_rate(self):
        material_type_set = set()
        materials_list = self._tmp['Materials']
        for material in materials_list:
            material_type_set.add(material['CookTag'])
        
        for item in self.system_data['SuperSuccessRateList']:
            if item['MaterialTypeNum'] == len(material_type_set):
                self._tmp['SuperSuccessRate'] = item['Rate']
                return
            
    def _selling_price(self):
        selling_price = 0
        materials_list = self._tmp['Materials']
        for material in materials_list:
            selling_price += material.get('SellingPrice', 0)
        for item in self.system_data['PriceRateList']:
            if item['MaterialNum'] == len(materials_list):
                self._tmp['SellingPrice'] = math.floor(selling_price * item['Rate'])
                return 
        return

    def _spice_boost(self):
        if self._tmp['Recipe']['ResultActorName'] == 'Item_Cook_O_01':
            return
        materials_list = self._tmp['Materials']
        effect = self._tmp.get('Effect')

        for material in materials_list:
            self._tmp['HitPointRecover'] += material.get('SpiceBoostHitPointRecover',0)
            self._tmp['EffectTime'] += material.get('SpiceBoostEffectiveTime',0)
            self._tmp['SuperSuccessRate'] += material.get('SpiceBoostSuccessRate',0)
            if effect and effect['EffectType'] == 'LifeMaxUp':
                self._tmp['EffectPotency'] += material.get('SpiceBoostMaxHeartLevel',0)
            if effect and effect['EffectType'] == 'StaminaRecover':
                self._tmp['EffectPotency'] += material.get('SpiceBoostMaxHeartLevel',0)
    

    def _craft(self):
        recipe = self._tmp['Recipe']
        effect = self._tmp.get('Effect')

        # recipe bonus
        # HitPointRecover
        if recipe['ResultActorName'] == 'Item_Cook_O_01':
            life_recover_rate = self.system_data['SubtleLifeRecoverRate']
        else:
            life_recover_rate = self.system_data['LifeRecoverRate']
        self._tmp['HitPointRecover'] = self._tmp['HitPointRecover'] * life_recover_rate + recipe.get('BonusHeart', 0)
        # EffectTime
        self._tmp['EffectTime'] += recipe.get('BonusTime',0)
        # EffectPotency
        self._tmp['EffectPotency'] += recipe.get('BonusLevel',0)


        # EffectLevel
        if effect:
            if not effect.get('LevelThreshold'):
                self._tmp['EffectTime'] = 0
                self._tmp['EffectLevel'] = self._tmp['EffectPotency']
            else:
                for level_threshold in effect.get('LevelThreshold'):
                    if self._tmp['EffectPotency'] >= level_threshold:
                        self._tmp['EffectLevel'] = effect.get('LevelThreshold').index(level_threshold) + 1
        else:
            self._tmp['EffectTime'] = 0
            self._tmp['EffectLevel'] = 0
        
        # Special Deal
        if recipe['ResultActorName'] == 'Item_Cook_O_02':
            self._tmp['HitPointRecover'] = 1
            self._tmp['Effect'] = None
            self._tmp['EffectTime'] = 0
            self._tmp['EffectLevel'] = 0
            self._tmp['SellingPrice'] = 2
        elif recipe['ResultActorName'] == 'Item_Cook_O_01':
            self._tmp['HitPointRecover'] = max(self.system_data['SubtleLifeRecover'], self._tmp['HitPointRecover'])
            self._tmp['Effect'] = None
            self._tmp['EffectTime'] = 0
            self._tmp['EffectLevel'] = 0
            self._tmp['SellingPrice'] = 2
        elif recipe['ResultActorName'] == 'Item_Cook_C_16':
            self._tmp['SellingPrice'] = 2
        elif recipe['ResultActorName'] == 'Item_Cook_C_17':
            self._tmp['HitPointRecover'] = 0

    def _locale(self):
        result_actor_name = self._tmp['Recipe']['ResultActorName']
        effect = self._tmp.get('Effect')

        locale_actor_name = self._locale_dict['Meal'][f'{result_actor_name}_Name'][self.area_lang]
        

        # name
        locale_effect_name = ''
        locale_buff_name = ''
        if effect:
            locale_effect_name = self._locale_dict['Effect'][effect['EffectType']+'_Name'][self.area_lang]
            locale_buff_name = self._locale_dict['Buff'][effect['EffectType']][self.area_lang]
        
        locale_meal_name = locale_effect_name + locale_actor_name

        # effect time
        minutes, seconds = divmod(self._tmp['EffectTime'], 60)
        effect_time_str = "{:02d}:{:02d}".format(int(minutes), int(seconds))

        # heart
        whole_heart, quarter_heart = divmod(self._tmp['HitPointRecover'], 4)
        whole_heart = int(whole_heart)
        quarter_heart = int(quarter_heart)
        quarter_heart_map = {
            0: '',
            1: '¼',
            2: '½',
            3: '¾'
        }
        if effect and effect['EffectType'] == 'LifeMaxUp':
            heart_str = '♥'+self._locale_dict['App']['FullRecovery_Name'][self.area_lang]
        else:
            heart_str = '♥' * whole_heart 
            if quarter_heart:
                heart_str += quarter_heart_map[quarter_heart]+'♥'
        
        # desc
        locale_actor_caption = self._locale_dict['Meal'][f'{result_actor_name}_Caption'][self.area_lang]
        locale_effect_desc = ''
        if effect:
            effect_desc_key = effect['EffectType']
            if result_actor_name == 'Item_Cook_C_17':
                effect_desc_key += '_MedicineDesc'
            else:
                effect_desc_key += '_Desc'
            
            if effect['MaxLv'] <= 3 and self._tmp['EffectLevel'] > 1:
                effect_desc_key += '_{:02d}'.format(self._tmp['EffectLevel'])
            locale_effect_desc = self._locale_dict['Effect'][effect_desc_key][self.area_lang]

        local_meal_desc = (locale_effect_desc +'\n' + locale_actor_caption).strip()


        self._result = {
            'MealName': locale_meal_name,
            'ActorName': self._tmp['Recipe']['ResultActorName'],
            'RecipeCardNum': self._tmp['Recipe']['PictureBookNum'],
            'HitPointRecover': heart_str,
            'EffectType': locale_buff_name,
            'EffectTime': effect_time_str,
            'EffectLevel': self._tmp['EffectLevel'],
            'SuperSuccessRate': min(self._tmp['SuperSuccessRate'] * 0.01, 1.00),
            'SellingPrice': self._tmp['SellingPrice'],
            'Caption': local_meal_desc,
        }
        # Item_Cook_C_17
        if result_actor_name == 'Item_Cook_C_17':
            self._result['ActorName'] += '_' + self._tmp['Effect']['EffectType']
            self._result['RecipeCardNum'] = self.recipe_card_table.index(self._result['ActorName']) + 1


        self.output = {}
        for k, v in self._result.items():
            al_k = self._locale_dict['App'][f'{k}_Name'][self.area_lang]
            if not al_k:
                al_k = k
            self.output[al_k] = v

# Test
if __name__ == '__main__':
    sim = TotkCookSim()
    output = sim.cook(['天空蘑菇'])
    print(output)
    output = sim.cook(['莱尼尔的刃角', '速速蜥蜴'])
    print(output)
    output = sim.cook(['兽肉', '高级兽肉','禽肉'])
    print(output)
    output = sim.cook(['钻石', '耐火蜥蜴'])
    print(output)
    output = sim.cook(['生命大萝卜'])
    print(output)
    output = sim.cook(['鲜奶'])
    print(output)
    output = sim.cook(['奥尔龙的犄角', '冰冷蜻蜓'])
    print(output)
    output = sim.cook(['古栗欧克的火焰犄角'])
    print(output)
    output = sim.cook(['速速青蛙', '霍拉布林的犄角'])
    print(output)