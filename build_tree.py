import json


class thetree:
    def __init__(self, weather_qst, list_businesses_rating, list_businesses_price):
        self.final_tree = \
            ("Would you like to sort by rating or price?",
             (weather_qst,
              (['I suggest you go today, this is the 5 restaurants sorted by rating:', list_businesses_rating], None, None),
              (['I suggest  you go tomorrow, this is the 5 restaurants sorted by rating:', list_businesses_rating], None,
               None)),
             (weather_qst,
              (['I suggest you go today, this is the 5 restaurants sorted by price:', list_businesses_price], None, None),
              (['I suggest you go tomorrow, this is the 5 restaurants sorted by price:', list_businesses_price], None,
               None)))

    def save_tree_json(self):
        # Serializing json
        json_object = json.dumps(self.final_tree, indent=4)

        # Writing to finalTree.json
        with open("finalTree.json", "w") as outfile:
            outfile.write(json_object)

