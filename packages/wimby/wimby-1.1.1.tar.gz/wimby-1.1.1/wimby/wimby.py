from statistics import mean

from shameni import Gaze
from namari import Namari
from arkivist import Arkivist

class Wimby:
    def __init__(self, coins, aliased=False, debug=False):
        debug = False
        if isinstance(debug, bool):
            self.debug = debug
        if isinstance(aliased, bool):
            self.aliased = aliased
        self.aliases = []
        if aliased:
            self.aliases = get_aliases(Gaze().supported())
        self.coins = _supported(coins, self.aliases, self.aliased, self.debug)
        self.momentum = _historical_averages(self.coins, self.debug)
        self.movers = _movements(self.momentum, self.debug)
    
    def change(self, coins):
        self.coins = _supported(coins, self.aliases, self.aliased, self.debug)

    def reload(self):
        self.momentum = _historical_averages(self.coins, self.debug)
        self.movers = _movements(self.momentum, self.debug)
    
    def dump(self):
        if self.movers.count() > 0:
            print("Wimby Cyrpocurrency Analysis")
            print("\n[NOTES]")
            print("A. Do your own research")
            print("B. Trade at your own risk")
            print("C. Consult a certified financial expert")
            print("\n[How to use these data?]")
            print("1. The ordered list denotes price movements as compared to the 3-day weighted averages.")
            print("2. Negative percentage means downward movement")
            print("    * Suggestive to BUY at your discretion")
            print("3. Positive percentage means upward movement")
            print("    * Suggestive to SELL at your discretion")
            print("4. The periodic trend pattern (+/-) denotes the 90, 60, 30, 15, 7, 3, 1-day weighted averages.")
            print("    * The more negative trends up to the rightmost WAVGs mean successive downward price movement.")
            print("        - Suggestive to STRONGLY BUY at your discretion")
            print("    * The more positive trends up to the rightmost WAVGs mean successive upward price movement.")
            print("        - Suggestive to STRONGLY SELL at your discretion")
            print("5. Your probable last metric would be on the Coinbase application.")
            print("    * More than 80% Sell Trend is suggestive to STRONGLY SELL at your discretion.")
            print("    * More than 60% Sell Trend is suggestive to SELL at your discretion.")
            print("    * More than 60% Buy Trend is suggestive to HOLD or strategic BUY at your discretion.")
            print("    * More than 80% Buy Trend is suggestive to HOLD or STRONGLY  BUY at your discretion.")
            print("6. Use the three (3) metrics to trade or hold strategically.")
            print("\n[WAVG Analytics]")
            ranking = list(sorted([float(x) for x in self.movers.keys()]))
            minn = len(str(int((min(ranking) * 100)))) + 3
            maxn = len(str(int((max(ranking) * 100)))) + 3
            padding = max([maxn, minn])
            for rank in ranking:
                tokens = self.movers.get(str(rank), [])
                movement = rank * 100
                for token in tokens:
                    fmovement = f"{movement:,.2f}"
                    while len(fmovement) < padding:
                        fmovement = f" {fmovement}"
                    print(f"{fmovement} {token}")
                    pattern = self.momentum.get(token, {}).get("trend", "")
                    if pattern.strip() != "":
                        print(f"    {pattern}")

def _supported(coins, aliases, aliased, debug):
    supported = []
    if isinstance(coins, list):
        if debug:
            print("Getting token aliases...")
        if aliased:
            for coin in coins:
                alias = aliases.get(coin)
                if alias is not None:
                    supported.append(alias)
        else:
            return coins
    return supported

def _movements(momentum, debug):
    if debug:
        print("Analyzing movements...")
    movers = Arkivist()
    for token, trends in momentum.items():
        price = trends.get("0", 0)
        wavg = trends.get("3", 0)
        if min(price, wavg) > 0:
            change = (price - wavg) / wavg
            tokens = movers.get(change, [])
            tokens.append(token)
            tokens = list(sorted(tokens))
            movers.set(str(change), tokens)
    return movers

def _historical_averages(coins, debug):
    if debug:
        print("Collecting periodic weighted averages...")
    momentum = Arkivist()
    prices = _prevailing(",".join(coins))
    wavgs = (90, 60, 30, 15, 7, 3, 1)
    for token in coins:
        trends = momentum.get(token, {})
        price = prices.get(token, {}).get("usd", 0)
        if price > 0:
            trends.update({"0": price})
            pattern = []
            for days in wavgs:
                wavg = trends.get(str(days), 0)
                if wavg <= 0:
                    wavg = _weighted_average(token, days=days)
                if wavg > 0:
                    trends.update({str(days): wavg})
                    if price > wavg:
                        pattern.append("+")
                    else:
                        pattern.append("-")
                else:
                    pattern.append(" ")
                
            trends.update({"trend": "".join(pattern)})
            momentum.set(token, trends)
    return momentum

def _prevailing(token):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd"
    return Arkivist().fetch(url)

def _weighted_average(token, days=1):
    weighted_avg = -1
    prices = []
    root = Arkivist().fetch(f"https://api.coingecko.com/api/v3/coins/{token}/market_chart?vs_currency=usd&days={days}&interval=daily").show()
    for price in root.get("prices", []):
        prices.append(float(price[1]))
        
    if len(prices) > 0:
        
        avg = mean(prices)
        avg_los = len([i for i in prices if i < avg])
        avg_his = len([i for i in prices if i > avg])
        avg_eql = len([i for i in prices if i == avg])
            
        ## get weighted average
        weighted_total = 0
        total_weights = 0
        for price in prices:
            if price < avg:
                weighted_total += (price * avg_los)
                total_weights += avg_los
            elif price > avg:
                weighted_total += (price * avg_his)
                total_weights += avg_his
            else:
                weighted_total += (price * avg_eql)
                total_weights += avg_eql
        weighted_avg = weighted_total / total_weights
    return weighted_avg

def get_aliases(supported):
    aliases = Namari()
    assets = Arkivist()
    for token in supported:
        asset = {}
        url = f"https://api.coingecko.com/api/v3/coins/{token}" \
            "?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"
        data = Arkivist().fetch(url).show()
        if isinstance(data, list):
            if len(data) > 0:
                asset = data[0]
        
        aliases.set(token, token)
        aliases.attach(token, token.lower())
        aliases.attach(token, token.upper())
        aliases.attach(token, token.title())
        aliases.attach(token, token.capitalize())
        
        if len(asset) > 0:
            symbol = asset.get("symbol", token)
            aliases.attach(token, symbol)
            aliases.attach(token, symbol.lower())
            aliases.attach(token, symbol.upper())
            aliases.attach(token, symbol.title())
            aliases.attach(token, symbol.capitalize())
            
            name = asset.get("name", token)
            aliases.attach(token, name)
            aliases.attach(token, name.lower())
            aliases.attach(token, name.upper())
            aliases.attach(token, name.title())
            aliases.attach(token, name.capitalize())
    return aliases