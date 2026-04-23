print("hello world")
print("wassup")
import random
import json


# Crop Class
class Crop:
    def __init__(self, crop_type, days_to_harvest, sell_price):
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

    def __str__(self):
        """
        String representation for printing crop status.
        """
        return f"{self.crop_type}: {self.days_grown}/{self.days_to_harvest} days, Health: {self.health}"
