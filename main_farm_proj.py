import os
import random
import json


# Crop Class
class Farm(): #Temi
    '''
    This class will hold the main strcuture of the farm such as the size, ability to increase, ability to plant crops (using grow method in crop class), and more.  
    '''
    def __init__(self, money, water, energy, crop_list, day) -> None:
        '''
        Initialize the variables of the Farm class
        '''
        self.money = money
        self.water = water
        self.energy = energy
        self.crop_list = crop_list
        self.day = day
        self.size = 10  # maximum number of crops
    
    def plant_crop(self, crop):
        """
        Plant a crop if there's space.
        """
        if len(self.crop_list) < self.size:
            self.crop_list.append(crop)
            return True
        return False
    
    def harvest_ready_crops(self):
        """
        Harvest all ready crops and return them.
        """
        harvested = []
        for crop in self.crop_list[:]:
            if crop.check_harvest_ready():
                harvested.append(crop)
                self.crop_list.remove(crop)
        return harvested
    
    def water_crops(self): #Raymond Quarshie
        """
        Water all crops.
        """
        if self.water >= 10:  # Check if enough water
            self.water -= 10   # Consume water
            for crop in self.crop_list:
                crop.apply_water()
            return True
        return False  # Not enough water
    
    def grow_crops(self):
        """
        Grow all crops by one day.
        """
        for crop in self.crop_list:
            crop.grow()
    
    def increase_size(self, amount):
        """
        Increase the farm size.
        """
        self.size += amount
    
    def __str__(self):
        """
        String representation of the farm.
        """
        return f"Farm: Size {self.size}, Crops: {len(self.crop_list)}, Month: {self.day}"


class Crop(): #Jacob
    def __init__(self, crop_type: str, months_to_harvest, sell_price):
        """
        Initializes crop with its basic attributes.

        crop_type: name of the crop (string)
        months_to_harvest: amount of months it takes to grow
        sell_price: base price
        """
        self.crop_type = crop_type
        self.months_to_harvest = months_to_harvest
        self.sell_price = sell_price

        self.months_grown = 0          # tracks growth
        self.health = 100            # crop health where 0 = dead
        self.watered_this_month = False   # if it was watered this month

    def grow(self): #Jacob
        """
        Simulates one month of growth.

        - If watered: crop grows and gains health
        - If not watered: crop loses health
        - Resets watered status after growth
        """
        if self.health <= 0:
            return  # dead crops = nothing

        if self.watered_this_month:
            self.months_grown += 1
            self.health = min(100, self.health + 10)
        else:
            self.health -= 30  # penalty for not watering

        self.watered_this_month = False  # reset for next month

    def apply_water(self): #Jacob
        """
        Marks crop as watered for the month.
        """
        self.watered_this_month = True

    def check_harvest_ready(self): #Jacob
        """
        Returns True if crop is ready to harvest.
        """
        return self.months_grown >= self.months_to_harvest and self.health > 0
    
    def inventory(self): #Temi
       '''
       This stores all the crop objects the player has.
       '''
       pass

    def __str__(self):
        """
        String representation for printing crop status.
        """
        return f"{self.crop_type}: {self.months_grown}/{self.months_to_harvest} months, Health: {self.health}"
    

class Player(): #Temi
    def __init__(self, name):
        '''
        Initialize the attributes for the Player class
        '''
        self.name = name
        self.energy = 50
        self.money = 1000
        
    def __str__(self):
        '''
        Print a summary of the player's stats.
        '''
        return f"{self.name} has {self.energy} energy left and {self.money} amount of money left."

    def add_money(self, amount): #Raymond Quarshie
        '''
        Adds money to player's balance
        '''
        self.money += amount
        return self.money 
        
    def display_stats(self):
        """
        Print current stats of player
        """
        print(f"Name: {self.name}")
        print(f"Money: ${self.money}")
        print(f"Energy: {self.energy}")
        print(f"Water: {self.water}" if hasattr(self, 'water') else "Water: Check Farm")
    
# Mamadou Niang

class Summary: # Mamadou Niang
    
    def __init__(self, playerName, finalMoney, crops_harvested, months, farm_size, version="1.0"):
        self.playerName = playerName  
        self.finalMoney = finalMoney
        self.crops_harvested = crops_harvested  # list of what was harvested
        self.months = months  # how many months they played
        self.farm_size = farm_size
        self.version = version
    
    def save_summary(self, filename="results.json"):
        summary_data = {
            "player": self.playerName,
            "money": self.finalMoney,
            "months_played": self.months,
            "crops": self.crops_harvested,
            "farm_size": self.farm_size,
            "version": self.version
        }
        with open(filename, "w") as f:
            json.dump(summary_data, f, indent=4)
        print(f"Summary saved to {filename}!")

    def load_and_print(self, filename="results.json"):
        if not os.path.exists(filename):
            print("no summary file found, did you save first?")
            return
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"\n===== GAME OVER =====")
        print(f"Player: {data['player']}")
        print(f"Months survived: {data['months_played']}")
        print(f"Final money: ${data['money']}")
        print(f"Farm size: {data['farm_size']}")
        print(f"Crops harvested: {', '.join(data['crops']) if data['crops'] else 'none lol'}")
        print(f"Version: {data['version']}")
        print(f"=====================\n")
    
    def __str__(self):
        return f"{self.playerName} finished with ${self.finalMoney} after {self.months} months, farm size {self.farm_size}"

    # Mamadou Niang - added rank_crops_by_value method
    # ranks harvested crops by profit score using a scoring algorithm
    # implements technique #9: sorted() with a lambda key function
    def rank_crops_by_value(self, crop_prices: dict) -> list:
        """
        Ranks harvested crops by total earned value using a scoring algorithm.
        score = (frequency * base_price) + consistency_bonus
        Consistency bonus rewards crops harvested more than twice.
        Uses technique #9: sorted() with a key function (lambda).
        """
        crop_counts = {}
        for crop in self.crops_harvested:
            crop_counts[crop] = crop_counts.get(crop, 0) + 1

        scored = []
        for crop_type, count in crop_counts.items():
            base_price = crop_prices.get(crop_type, 0)
            consistency_bonus = (count - 2) * (base_price * 0.15) if count > 2 else 0
            score = (count * base_price) + consistency_bonus
            scored.append((crop_type, round(score, 2)))

        return sorted(scored, key=lambda item: item[1], reverse=True)