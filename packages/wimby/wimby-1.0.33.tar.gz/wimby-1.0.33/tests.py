from wimby import Wimby
from shameni import Gaze

coins = Gaze().supported()
crypto = Wimby(coins, debug=True)
crypto.dump()

# arkivist object
momentum = crypto.momentum

# arkivist object
movers = crypto.movers

