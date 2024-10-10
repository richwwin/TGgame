import random
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['space_claw_game']

class GameLogic:
    def __init__(self):
        self.prizes = db.prizes
        self.users = db.users

    def calculate_grab_result(self, user_id, grab_type):
        user = self.users.find_one({'telegram_id': user_id})
        if not user:
            return None

        probabilities = {
            'small': 0.6,
            'medium': 0.3,
            'large': 0.1
        }

        attempts = {
            'one': 1,
            'five': 5,
            'ten': 10
        }.get(grab_type, 1)

        results = []
        for _ in range(attempts):
            if random.random() < 0.95:  # 95% 機會抓到商品
                prize_type = random.choices(list(probabilities.keys()), 
                                            weights=list(probabilities.values()))[0]
                prize = self.prizes.find_one({'type': prize_type, 'stock': {'$gt': 0}})
                if prize:
                    self.prizes.update_one({'_id': prize['_id']}, {'$inc': {'stock': -1}})
                    results.append(prize)

        self.users.update_one({'telegram_id': user_id}, 
                              {'$inc': {'score': len(results) * 10}})

        return results

game_logic = GameLogic()