class Configuration:
    def __init__(self, buy=0, sell=1, coin_first=0, coin_second=1, percent=0.2):
        self.__buy = int(buy)
        self.__sell = int(sell)
        self.__coin_first = int(coin_first)
        self.__coin_second = int(coin_second)
        self._percent = float(percent)

    @property
    def buy(self):
        return self.__buy

    @property
    def sell(self):
        return self.__sell

    @property
    def coin_first(self):
        return self.__coin_first

    @property
    def coin_second(self):
        return self.__coin_second

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, percent):
        self._percent = percent
