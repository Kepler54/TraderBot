from data_base import DataBase


class DataAnalysis(DataBase):
    def coin_trade_info(self, buy_or_sell) -> list:
        """
        The function divides currency pairs accepted as a tuple into separate buy and sell lists
        :param buy_or_sell: object
        :return: str
        """
        values_list = self.get_value_list("SELECT buy, sell FROM trades")
        value_list = []
        for value in values_list:
            value_list.append(float(value[buy_or_sell]))
        return value_list

    def percentage(self, value, buy_or_sell) -> tuple[str, str]:
        """
        The function returns the percentage ratio
        :param value: list
        :param buy_or_sell: object
        :return: list
        """
        return (
            f'{float(f"{value / self.coin_trade_info(buy_or_sell)[0]:%}"[0:-1]) - 100:.8f}',
            f'{value / self.coin_trade_info(buy_or_sell)[0]:%}'
        )

    def buy_sell_verify(self) -> str:
        """
        The function returns the decision to buy or sell the coin
        :return: str
        """
        if float(self.percentage(self.coin_trade_info(self.sell)[-1], self.sell)[0]) >= 1.0:
            return f", нужно покупать [{self.get_coin_name(self.coin_second)}]"
        elif float(self.percentage(self.coin_trade_info(self.buy)[-1], self.buy)[0]) <= -1.0:
            return f", нужно покупать [{self.get_coin_name(self.coin_first)}]"
        else:
            return ''

    def get_exchange_info(self, value, buy_or_sell) -> str:
        """
        The function takes a list consisting of coin values and returns the percentage ratio
        of the last element of the list to the first one
        :param value: list
        :param buy_or_sell: object
        :return: str
        """
        if len(self.coin_trade_info(buy_or_sell)) != 1:
            if f'{float(self.percentage(value, buy_or_sell)[1][0:-1]) - 100}'[0:5][0] == '-':
                return (
                    f"Изменение стоимости [{self.get_coin_name(self.coin_first)}] по отношению к "
                    f"[{self.get_coin_name(self.coin_second)}] {self.coin_trade_info(buy_or_sell)[-1]} "
                    f"составило: {float(self.percentage(value, buy_or_sell)[1][0:-1]) - 100:.8f}% ↓"
                )
            elif float(self.percentage(value, buy_or_sell)[1][0:-1]) - 100 == 0.0:
                return (
                    f"Стоимость [{self.get_coin_name(self.coin_first)}] не изменилась "
                    f"{self.coin_trade_info(buy_or_sell)[-1]} [{self.get_coin_name(self.coin_second)}]"
                )
            else:
                return (
                    f"Изменение стоимости [{self.get_coin_name(self.coin_first)}] по отношению к "
                    f"[{self.get_coin_name(self.coin_second)}] {self.coin_trade_info(buy_or_sell)[-1]} "
                    f"составило: {float(self.percentage(value, buy_or_sell)[1][0:-1]) - 100:.8f}% ↑"
                )
        else:
            return (
                f"Стоимость [{self.get_coin_name(self.coin_first)}] на начало торгов составила "
                f"{self.coin_trade_info(buy_or_sell)[0]} [{self.get_coin_name(self.coin_second)}]"
            )

    def get_full_info(self) -> str:
        """
        The function takes the initial number of coins and returns the result at the current exchange rate
        :return: str
        """
        amount = float(self.get_value_list("SELECT amount FROM trades")[0][0])
        percent = float(self.get_value_list("SELECT percent FROM trades")[0][0])

        start_price = amount * self.coin_trade_info(self.buy)[0]
        start_price_minus_percent = float(start_price - (start_price / 100 * percent))

        current_price = amount * self.coin_trade_info(self.buy)[-1]
        current_price_minus_percent = float(current_price - (current_price / 100 * percent))

        return (
            f"Сумма входа в {self.get_coin_name(self.coin_first)}: {amount:.8f}\n"
            f"Комиссия составляет: {percent}%\n"
            f"Начальный результат в {self.get_coin_name(self.coin_second)}: {start_price_minus_percent:.8f}\n"
            f"Актуальный результат в {self.get_coin_name(self.coin_second)}: {current_price_minus_percent:.8f}\n"
            f"Изменение суммы: {current_price_minus_percent - start_price_minus_percent:.8f}{self.buy_sell_verify()}\n"
            f"(Продажа) {self.get_exchange_info(self.coin_trade_info(self.buy)[-1], self.buy)}\n"
            f"(Покупка) {self.get_exchange_info(self.coin_trade_info(self.sell)[-1], self.sell)}\n"
        )
