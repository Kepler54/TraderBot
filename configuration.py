class Descriptor:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        return getattr(instance, self.name)


class Configuration:
    buy = Descriptor()
    sell = Descriptor()
    coin_first = Descriptor()
    coin_second = Descriptor()

    @classmethod
    def verify_instance(cls, instance):
        if type(instance) != float:
            raise TypeError

    def __init__(self, buy=0, sell=1, coin_first=0, coin_second=1, percent=0.2):
        self._buy = buy
        self._sell = sell
        self._coin_first = coin_first
        self._coin_second = coin_second
        self._percent = percent

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, instance):
        self.verify_instance(instance)
        self._percent = instance
