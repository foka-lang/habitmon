import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    SUBSCRIPTION_PRICES = {
        '1month': 61,
        '3months': 127,
        '6months': 235
    }

    SUBSCRIPTION_PRICES_POINTS = {
        '1month': 610,
        '3months': 1270,
        '6months': 2350
    }

    MONTHLY_TOP_REWARDS = {
        1: 5000, 2: 4500, 3: 4000, 4: 3500, 5: 3000,
        6: 2500, 7: 2000, 8: 1500, 9: 1000, 10: 500
    }

    @staticmethod
    def get_xp_for_place(place):
        if place < 1 or place > 100:
            return 0
        return max(10, 1000 - (place - 1) * 10)

    XP_PER_HABIT = 20

    STREAK_REWARDS = {
        100: 1000, 200: 2000, 300: 3000, 400: 4000,
        500: 5000, 600: 6000, 700: 7000, 800: 8000,
        900: 9000, 1000: 10000
    }

    STREAK_POINTS_REWARDS = {
        100: 1000, 200: 2000, 300: 3000, 400: 4000,
        500: 5000, 600: 6000, 700: 7000, 800: 8000,
        900: 9000, 1000: 10000
    }

    REFERRAL_BONUS_POINTS = 250
    MAX_LEVEL = 1000

    @staticmethod
    def xp_needed_for_level(level):
        return level * 50