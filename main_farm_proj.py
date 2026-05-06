import os
import random
import json


# Crop Class
class Farm(): #Temi
    '''
    Farm holds the current state of the farm and provides actions for planting,
    watering, growing, and harvesting crops.
    Args:
        money (int): Starting money available to the farm.
        water (int): Current water supply for crop care.
        energy (int): Energy available for farm operations.
        crop_list (list[Crop]): List of planted crops on the farm.
        day (int): Current day or month count in the game.
    Returns:
        None
    '''
    def __init__(self, money, water, energy, crop_list, day) -> None:
        '''
        Initialize the Farm instance.
        Args:
            money (int): Starting money available to the farm.
            water (int): Initial water supply.
            energy (int): Initial energy level.
            crop_list (list[Crop]): Initial list of crops.
            day (int): Starting day or month count.
        Returns:
            None
        '''
        self.money = money
        self.water = water
        self.energy = energy
        self.crop_list = crop_list
        self.day = day
        self.size = 10  # maximum number of crops
    
    def plant_crop(self, crop):
        '''
        Plant a crop if there is room on the farm.
        Args:
            crop (Crop): Crop instance to plant.
        Returns:
            bool: True if the crop was planted, False if the farm is full.
        '''
        if len(self.crop_list) < self.size:
            self.crop_list.append(crop)
            return True
        return False
    
    def harvest_ready_crops(self):
        '''
        Harvest all crops that are ready to harvest.
        Returns:
            list[Crop]: List of harvested crop instances.
        '''
        harvested = []
        for crop in self.crop_list[:]:
            if crop.check_harvest_ready():
                harvested.append(crop)
                self.crop_list.remove(crop)
        return harvested
    
    def water_crops(self):
        '''
        Water all planted crops.
        Returns:
            None
        '''
        for crop in self.crop_list:
            crop.apply_water()
    
    def grow_crops(self):
        '''
        Advance growth for all crops by one month.
        Returns:
            None
        '''
        for crop in self.crop_list:
            crop.grow()
    
    def increase_size(self, amount):
        '''
        Increase the farm's maximum crop capacity.
        Args:
            amount (int): Number of additional crop slots.
        Returns:
            None
        '''
        self.size += amount
    
    def __str__(self):
        '''
        Return a human-readable summary of the farm.
        Returns:
            str: Farm summary string.
        '''
        return f"Farm: Size {self.size}, Crops: {len(self.crop_list)}, Month: {self.day}"
class Crop(): #Jacob
    '''
    Crop represents a planted crop with growth, health, and harvest state.
    Args:
        crop_type (str): Type of crop, such as wheat or corn.
        months_to_harvest (int): Months required before the crop can be harvested.
        sell_price (int): Money gained when the crop is harvested.
    Returns:
        None
    '''
    def __init__(self, crop_type: str, months_to_harvest, sell_price):
        '''
        Initialize a Crop instance.
        Args:
            crop_type (str): The crop's name or type.
            months_to_harvest (int): Number of months needed to mature.
            sell_price (int): Base selling price when harvested.
        Returns:
            None
        '''
        self.crop_type = crop_type
        self.months_to_harvest = months_to_harvest
        self.sell_price = sell_price

        self.months_grown = 0          # tracks growth
        self.health = 100            # crop health where 0 = dead
        self.watered_this_month = False   # if it was watered this month

    def grow(self): #Jacob
        '''
        Apply monthly growth effects to the crop.
        Returns:
            None
        '''
        if self.health <= 0:
            return  # dead crops = nothing

        if self.watered_this_month:
            self.months_grown += 1
            self.health = min(100, self.health + 10)
        else:
            self.health -= 30  # penalty for not watering

        self.watered_this_month = False  # reset for next month

    def apply_water(self): #Jacob
        '''
        Mark the crop as watered for the current month.
        Returns:
            None
        '''
        self.watered_this_month = True

    def check_harvest_ready(self): #Jacob
        '''
        Check whether the crop has grown enough and is still healthy.
        Returns:
            bool: True if the crop is ready to harvest, otherwise False.
        '''
        return self.months_grown >= self.months_to_harvest and self.health > 0


    def __str__(self):
        '''
        Return a string describing the crop's growth and health.
        Returns:
            str: Crop status string.
        '''
        return f"{self.crop_type}: {self.months_grown}/{self.months_to_harvest} months, Health: {self.health}"
    

class Player(): #Temi
    '''
    Player stores the current player name, energy, and money balance.
    Args:
        name (str): Name of the player.
    Returns:
        None
    '''
    def __init__(self, name):
        '''
        Initialize a Player instance.
        Args:
            name (str): The player's name.
        Returns:
            None
        '''
        self.name= name
        self.energy = 50
        self.money = 1000
    def __str__(self):
        '''
        Return a summary of the player's current stats.
        Returns:
            str: Player stats summary.
        '''
        return f"{self.name} has {self.energy} energy left and {self.money} amount of money left."

    def add_money(self, amount): #Raymond Quarshie
        '''
        Add money to the player's balance.
        Args:
            amount (int): Amount to add to the player's money.
        Returns:
            int: Updated money balance.
        '''
        self.money += amount
        return self.money 
        
    def display_stats(self):
        '''
        Print the player's current money and energy.
        Returns:
            None
        '''
        print(f"Name: {self.name}")
        print(f"Money: ${self.money}")
        print(f"Energy: {self.energy}")
    
# Mamadou Niang

class Summary: # Mamadou Niang
    '''
    Summary captures end-of-game results and can save or print them.
    Args:
        playerName (str): Name of the player.
        finalMoney (int): Final money balance at game end.
        crops_harvested (list[str]): Names of harvested crops.
        months (int): Number of months played.
        farm_size (int): Final farm capacity.
        version (str): Summary format version.
    Returns:
        None
    '''
    
    def __init__(self, playerName, finalMoney, crops_harvested, months, farm_size, version="1.0"):
        self.playerName = playerName  
        self.finalMoney = finalMoney
        self.crops_harvested = crops_harvested  # list of what was harvested
        self.months = months  # how many months they played
        self.farm_size = farm_size
        self.version = version
    
    def save_summary(self, filename="results.json"):
        '''
        Save the summary data to a JSON file.
        Args:
            filename (str): Name of the file to save the summary.
        Returns:
            None
        '''
        summary_data = {
            "player": self.playerName,
            "money": self.finalMoney,
            "months_played": self.months,
            "crops": self.crops_harvested,  # whatever they harvested
            "farm_size": self.farm_size,
            "version": self.version
        }
        
        with open(filename, "w") as f:
            json.dump(summary_data, f, indent=4)  # indent makes it readable i think
        
        print(f"Summary saved to {filename}!")  # just so player knows it worked

    def load_and_print(self, filename="results.json"):
        '''
        Load summary data from a file and print it.
        Args:
            filename (str): Name of the file to load the summary from.
        Returns:
            None
        '''
        if not os.path.exists(filename):
            print("no summary file found, did you save first?")
            return
        
        with open(filename, "r") as f:
            data = json.load(f)  # TODO: maybe add error handling later
        
        print(f"\n===== GAME OVER =====")
        print(f"Player: {data['player']}")
        print(f"Months survived: {data['months_played']}")
        print(f"Final money: ${data['money']}")
        print(f"Farm size: {data['farm_size']}")
        print(f"Crops harvested: {', '.join(data['crops']) if data['crops'] else 'none lol'}")
        print(f"Version: {data['version']}")
        print(f"=====================\n")
    
    def __str__(self):
        '''
        Return a concise summary of the final game results.
        Returns:
            str: Summary string.
        '''
        return f"{self.playerName} finished with ${self.finalMoney} after {self.months} months, farm size {self.farm_size}"
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
    
def main():
    '''
    Run the main farm game loop: Complete farm simulator game with monthly cycles, random events, and expansion

- Update Crop class to use monthly growth instead of daily
- Implement Farm class methods for planting, harvesting, watering, growing, and expanding
- Add random events each month affecting crop health and yields
- Introduce farm expansion feature to increase crop capacity
- Change game loop to 12-month cycle with early end option
- Update Summary class to track farm size and game version in results.json
- Integrate all classes in main function for full gameplay actions and game events.
    Returns:
        None
    '''
    name = input("Please enter your name: ")
    player = Player(name)
    print("Welcome to the Farm Game!")
    
    # Define available crops
    crops_available = {
        "wheat": {"months": 1, "price": 10, "cost": 5},
        "corn": {"months": 2, "price": 20, "cost": 10},
        "tomato": {"months": 1, "price": 15, "cost": 7}
    }
    
    farm = Farm(0, 100, 0, [], 1)  # money and energy managed by player
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
        
        player.display_stats()
        print(f"Farm: {farm}")
        print("Your crops:")
        for i, crop in enumerate(farm.crop_list):
            print(f"{i+1}. {crop}")
        
        print("\nActions:")
        print("1. Plant a crop")
        print("2. Water crops")
        print("3. Harvest ready crops")
        print("4. Expand farm")
        print("5. End game early")
        
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
                player.energy -= energy_cost
                farm.water_crops()
                print("All crops watered!")
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
        
        elif choice == "5":
            print("Ending game early...")
            break
        
        else:
            print("Invalid choice!")
        
        # End of month
        farm.grow_crops()
        month += 1
        farm.day = month
        player.energy = min(50, player.energy + 15)  # regain energy
        
        if player.money <= 0:
            print("Game over! Out of money.")
            break
    
    # Game over
    summary = Summary(player.name, player.money, harvested_crops, month - 1, farm.size)
    summary.save_summary()
    summary.load_and_print()

if __name__ == "__main__":
    main()
