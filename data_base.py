import sqlite3 as sq
from ast import literal_eval
from datetime import datetime
from trade_info import TradeInfo


class DataBase(TradeInfo):
    def create_db(self) -> None:
        """
        Create DB function
        :return: None
        """
        with sq.connect("trades.db") as db:
            cur = db.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS trades
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                date TEXT, time TEXT, coin_pair TEXT, buy TEXT, sell TEXT, amount TEXT, percent TEXT
                )
                """
            )
            cur.execute(
                "INSERT INTO trades VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)",
                (f'{datetime.now():%d}.{datetime.now():%m}.{datetime.now():%Y}',
                 f'{datetime.now():%H}:{datetime.now():%M}', self.get_coin_pair_amount()[0],
                 literal_eval(self.get_ticker(self.get_coin_pair_amount()[0]))[self.get_coin_pair_amount()[0]]["buy"],
                 literal_eval(self.get_ticker(self.get_coin_pair_amount()[0]))[self.get_coin_pair_amount()[0]]["sell"],
                 self.get_coin_pair_amount()[1], self.percent)
            )

    def get_data_db(self, coin_pair, amount) -> None:
        """
        Input data in DB function
        :param coin_pair: object
        :param amount: str
        :return: None
        """
        with sq.connect("trades.db") as db:
            cur = db.cursor()
            cur.execute(
                "INSERT INTO trades VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)",
                (
                    f'{datetime.now():%d}.{datetime.now():%m}.{datetime.now():%Y}',
                    f'{datetime.now():%H}:{datetime.now():%M}', coin_pair["coin_pair_state"],
                    literal_eval(self.get_ticker(coin_pair["coin_pair_state"]))[coin_pair["coin_pair_state"]]["buy"],
                    literal_eval(self.get_ticker(coin_pair["coin_pair_state"]))[coin_pair["coin_pair_state"]]["sell"],
                    amount["amount_state"], self.percent
                )
            )

    @staticmethod
    def get_value_list(select) -> list:
        """
        The function accepts a query to the database and returns a list of data
        :param select: str
        :return: list
        """
        with sq.connect(f"trades.db") as db:
            cur = db.cursor()
            cur.execute(select)
            return cur.fetchall()

    def get_coin_name(self, coin) -> str:
        """
        The function removes the "_" sign from the coin pair
        :param coin: object
        :return: str
        """
        coin_pair = self.get_value_list("SELECT coin_pair FROM trades")
        return (''.join(coin_pair[0][0])).split("_")[coin]

    def get_coin_pair_amount(self) -> list:
        """
        Return coin pair and amount function
        :return: list
        """
        coin_pair_and_amount = self.get_value_list("SELECT coin_pair, amount FROM trades")
        return coin_pair_and_amount[0]

    def get_buy_or_sell(self, buy_or_sell) -> list:
        """
        Return buy and sell objects and amount function
        :param buy_or_sell:
        :return: list
        """
        values_list = self.get_value_list("SELECT buy, sell FROM trades")
        value_list = []
        for value in values_list:
            value_list.append(float(value[buy_or_sell]))
        return value_list
