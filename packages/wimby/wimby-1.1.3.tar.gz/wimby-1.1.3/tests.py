from wimby import Wimby
from shameni import Gaze
from maguro import Maguro

coins = Maguro("coins.csv", delimiter=",")
if coins.count() ==0:
    coins.load(Gaze().supported())
crypto = Wimby(coins.unpack(), debug=True)
crypto.dump()

# arkivist object
momentum = crypto.momentum

# arkivist object
movers = crypto.movers

