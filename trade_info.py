import requests
from configuration import Configuration


class TradeInfo(Configuration):
    @staticmethod
    def get_ticker(coin_pair) -> str:
        """
        The function returns information about a pair or pairs in the last 24 hours
        :return: str
        """
        response = requests.get(url=f"https://yobit.net/api/3/ticker/{coin_pair}?ignore_invalid=1")
        return response.text
