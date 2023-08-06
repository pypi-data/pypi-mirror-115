from wimby import Wimby
from shameni import Gaze
from maguro import Maguro


yesterday = {"0.01": ["bitcoin"]}
coins = Maguro("coins.csv", delimiter=",")
if coins.count() ==0:
    coins.load(Gaze().supported())
crypto = Wimby(coins.unpack(), debug=True)
crypto.dump(yesterday)

# arkivist object
momentum = crypto.momentum

# arkivist object
movers = crypto.movers

