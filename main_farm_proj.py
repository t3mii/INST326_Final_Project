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
        
    def display_stats(self, farm):  # FIXED: farm parameter added
        """
        Print current stats of player
        """
        print(f"Name: {self.name}")
        print(f"Money: ${self.money}")
        print(f"Energy: {self.energy}")
        print(f"Water: {farm.water}")  # FIXED: uses farm.water


class Summary: # Mamadou Niang
    
    def __init__(self, playerName, finalMoney, crops_harvested, months, farm_size, version="1.0"):
        self.playerName = playerName  
        self.finalMoney = finalMoney
        self.crops_harvested = crops_harvested  # list of what was harvested
        self.months = months  # how many months they played
        self.farm_size = farm_size
        self.version = version
    
    def save_summary(self, filename="results.json"):
        # builds the summary dict to dump into json
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
        # loads the file back and prints it out
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


def main():
    name = input("Please enter your name: ")
    player = Player(name)
    print("Welcome to the Farm Game!")
    
    # Define available crops
    crops_available = {
        "wheat": {"months": 1, "price": 10, "cost": 5},
        "corn": {"months": 2, "price": 20, "cost": 10},
        "tomato": {"months": 1, "price": 15, "cost": 7}
    }
    
    farm = Farm(0, 100, 0, [], 1)
    month = 1
    harvested_crops = []
    
    while month <= 12:
        # Random event at start of month
        events = [
            ("Good rain", "All crops are automatically watered this month!"),
            ("Drought", "Crops lose extra health due to drought."),
            ("Pests", "Pests damage crops, reducing health."),
            ("Sunny weather", "Normal month, no special effects."),
            ("Bountiful harvest", "Harvest yields are doubled this month!")
        ]
        event_name, event_desc = random.choice(events)
        print(f"\n--- Month {month}: {event_name} ---")
        print(event_desc)
        
        # Apply event effects
        if event_name == "Good rain":
            farm.water_crops()
        elif event_name == "Drought":
            for crop in farm.crop_list:
                crop.health -= 20
        elif event_name == "Pests":
            for crop in farm.crop_list:
                crop.health -= 15
        
        player.display_stats(farm)  # FIXED: passing farm parameter
        print(f"Farm: {farm}")
        print("Your crops:")
        for i, crop in enumerate(farm.crop_list):
            print(f"{i+1}. {crop}")
        
        print("\nActions:")
        print("1. Plant a crop")
        print("2. Water crops")
        print("3. Harvest ready crops")
        print("4. Expand farm")
        print("5. Refill water ($10)")
        print("6. End game early")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print("Available crops:")
            for name, info in crops_available.items():
                print(f"{name}: Cost ${info['cost']}, Harvest in {info['months']} months, Sell for ${info['price']}")
            crop_choice = input("Which crop to plant? ").strip().lower()
            if crop_choice in crops_available:
                cost = crops_available[crop_choice]["cost"]
                if player.money >= cost:
                    player.money -= cost
                    new_crop = Crop(crop_choice, crops_available[crop_choice]["months"], crops_available[crop_choice]["price"])
                    if farm.plant_crop(new_crop):
                        print(f"Planted {crop_choice}!")
                    else:
                        print("Farm is full! Cannot plant more crops.")
                else:
                    print("Not enough money!")
            else:
                print("Invalid crop!")
        
        elif choice == "2":
            energy_cost = 10
            if player.energy >= energy_cost:
                if farm.water_crops():
                    player.energy -= energy_cost
                    print("All crops watered! Water remaining:", farm.water)
                else:
                    print("Not enough water! (Need 10 water)")
            else:
                print("Not enough energy!")
        
        elif choice == "3":
            ready_crops = farm.harvest_ready_crops()
            multiplier = 2 if event_name == "Bountiful harvest" else 1
            if ready_crops:
                for crop in ready_crops:
                    player.money += crop.sell_price * multiplier
                    harvested_crops.append(crop.crop_type)
                print(f"Harvested {len(ready_crops)} crops! (Multiplier: {multiplier})")
            else:
                print("No crops ready to harvest.")
        
        elif choice == "4":
            expand_cost = 100
            if player.money >= expand_cost:
                player.money -= expand_cost
                farm.increase_size(5)
                print("Farm expanded! Size increased by 5.")
            else:
                print("Not enough money to expand!")

        elif choice == "5": #water refile
            if player.money >= 10:
                player.money -= 10
                farm.water = min(200, farm.water + 50)
                print(f"Water refilled! Now at {farm.water}")
            else:
                print("Not enough money! Need $10")
                
        elif choice == "6":
            print("Ending game early...")
            break
        
        else:
            print("Invalid choice!")
        
        # End of month
        farm.grow_crops()
        month += 1
        farm.day = month
        player.energy = min(50, player.energy + 15)
        
        if player.money <= 0:
            print("Game over! Out of money.")
            break
    
    # Game over
    summary = Summary(player.name, player.money, harvested_crops, month - 1, farm.size)
    summary.save_summary()
    summary.load_and_print()


if __name__ == "__main__":
    main()
