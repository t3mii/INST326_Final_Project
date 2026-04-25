import os
import random
import json


# Crop Class
class Farm(): #Temi
    '''
    This class will hold the main strcuture of the farm such as the size, ability to increase, ability to plant crops (using grow method in crop class), and more.  
    '''
    def __init__(self) -> None:
        pass
class Crop(Farm):
    def __init__(self, crop_type: str, days_to_harvest, sell_price):
        """
        Initializes crop with its basic attributes.

        crop_type: name of the crop (string)
        days_to_harvest: amount of days it takes to grow
        sell_price: base price
        """
        self.crop_type = crop_type
        self.days_to_harvest = days_to_harvest
        self.sell_price = sell_price

        self.days_grown = 0          # tracks growth
        self.health = 100            # crop health where 0 = dead
        self.watered_today = False   # if it was watered this day

    def grow(self):
        """
        Simulates one day of growth.

        - If watered: crop grows faster and gains health
        - If not watered: crop loses health
        - Resets watered status after growth
        """
        if self.health <= 0:
            return  # dead crops = nothing

        if self.watered_today:
            self.days_grown += 1
            self.health = min(100, self.health + 5)
        else:
            self.health -= 15  # penalty for not watering

        self.watered_today = False  # reset for next day

    def apply_water(self):
        """
        Marks crop as watered for the day.
        """
        self.watered_today = True

    def check_harvest_ready(self):
        """
        Returns True if crop is ready to harvest.
        """
        return self.days_grown >= self.days_to_harvest and self.health > 0
    
    def inventory(self): #Temi
       '''
       This stores all the crop objects the player has.
       '''
       pass

    def __str__(self):
        """
        String representation for printing crop status.
        """
        return f"{self.crop_type}: {self.days_grown}/{self.days_to_harvest} days, Health: {self.health}"
    

class Player(): #Temi
    def __init__(self, name, money):
        self.name= name
        self.energy = 50
        self.money = 1000
    def __str__(self):
        return f"{self.name} has {self.energy} energy left and {self.money} amount of money left."

    def add_money(self, amount) #Raymond Quarshie
        """"
        Adds money to player's balance
        """"
        self.money += amount
        return self.money 
    
    
# Mamadou Niang

# Summary class - handles end of game recap
class Summary: # Mamadou Niang
    
    def __init__(self, playerName, finalMoney, crops_harvested, days):
        self.playerName = playerName  
        self.finalMoney = finalMoney
        self.crops_harvested = crops_harvested  # list of what was harvested
        self.days = days  # how many days they played
    
    def save_summary(self, filename="farm_summary.json"):
        # builds the summary dict to dump into json
        summary_data = {
            "player": self.playerName,
            "money": self.finalMoney,
            "days_played": self.days,
            "crops": self.crops_harvested  # whatever they harvested
        }
        
        with open(filename, "w") as f:
            json.dump(summary_data, f, indent=4)  # indent makes it readable i think
        
        print(f"Summary saved to {filename}!")  # just so player knows it worked

    def load_and_print(self, filename="farm_summary.json"):
        # loads the file back and prints it out, kinda like a receipt
        if not os.path.exists(filename):
            print("no summary file found, did you save first?")
            return
        
        with open(filename, "r") as f:
            data = json.load(f)  # TODO: maybe add error handling later
        
        # f-string to print out the final results
        print(f"\n===== GAME OVER =====")
        print(f"Player: {data['player']}")
        print(f"Days survived: {data['days_played']}")
        print(f"Final money: ${data['money']}")
        print(f"Crops harvested: {', '.join(data['crops']) if data['crops'] else 'none lol'}")
        print(f"=====================\n")
    
    def __str__(self):
        # magic method so you can just print the object if needed
        return f"{self.playerName} finished with ${self.finalMoney} after {self.days} days"

