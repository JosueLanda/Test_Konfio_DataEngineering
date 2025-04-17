import requests
import pandas as pd
from datetime import datetime
import datapipeline_konfio.base.extractor as extractor
import datapipeline_konfio.base.exceptions as exceptions
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from typing import Dict


class ExtractorCoinGecko(extractor.Extractor):
    def __init__(
        self,
        sparksession: SparkSession,
        date_range: Dict[str, str],
        api_demo_key: str,
        coint_to_search: str,
    ) -> None:

        self._urls_coingecko = {
            "endpoint_coin_list": "https://api.coingecko.com/api/v3/coins/list",
            "endpoint_market_chat": "https://api.coingecko.com/api/v3/coins/coin_value_id/market_chart/range",
        }

        self._date_range = {
            "from_date": int(date_range["from_date"].timestamp()),
            "to_date": int(date_range["to_date"].timestamp()),
        }
        self._api_demo_key = api_demo_key
        self._coint_to_search = coint_to_search
        self._sparksession = sparksession

        self._parameter_validation()
        self._perform_to_authentication()

    def _parameter_validation(self) -> None:
        pass

    def _perform_to_authentication(self) -> None:

        """_summary_

        Raises:
            exceptions.ExtractorErrorAuthentication: _description_
        """

        params = {
            "vs_currency": "usd",
            "from": self._date_range.get("from_date"),
            "to": self._date_range.get("to_date"),
            "x_cg_demo_api_key": self._api_demo_key,
        }

        self._request_coint_list = requests.get(
            self._urls_coingecko.get("endpoint_coin_list"),
            headers={"User-Agent": "Mozilla/5.0"},
        )
        self._construction_coint_id()
        self._request_market_chat = requests.get(
            self._urls_coingecko.get("endpoint_market_chat").replace(
                "coin_value_id", self._coint_id
            ),
            params=params,
        )

        endpoints = {
            "coint_list": self._request_coint_list,
            "market_chat": self._request_market_chat,
        }

        for name, response in endpoints.items():
            if response.status_code != 200:
                raise exceptions.ExtractorErrorAuthentication(
                    f"Error de autenticación para el endpoint {name}"
                )

    def _construction_coint_id(self) -> str:

        """_summary_
        """

        # ================================= Construccion =================================START

        data_coint_list = self._request_coint_list.json()

        data_coint_list = [
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "symbol": item.get("symbol"),
            }
            for item in data_coint_list
            if "id" in item and "name" in item and "symbol" in item
        ]

        df_coint_list = pd.DataFrame(data_coint_list)

        # ================================= Construccion =================================END

        # ================================= Setteado de valores =================================START

        df_coint_list = df_coint_list[df_coint_list["name"] == self._coint_to_search]

        self._coint_id = (
            df_coint_list.iloc[0]["id"] if not df_coint_list.empty else None
        )
        self._symbol = (
            df_coint_list.iloc[0]["symbol"] if not df_coint_list.empty else None
        )
        self._name = df_coint_list.iloc[0]["name"] if not df_coint_list.empty else None

        # ================================= Setteado de valores =================================END

    def extract_data_from_source(self) -> DataFrame:
        
        """_summary_

        Returns:
            _type_: _description_
        """

        data = self._request_market_chat.json()
        prices = data.get("prices", [])

        if not prices:
            return self._sparksession.createDataFrame(pd.DataFrame())

        # Procesar todos los precios con su fecha y timestamp original
        processed = []
        for ts, price in prices:
            date = datetime.utcfromtimestamp(ts / 1000).date()
            processed.append(
                {
                    "timestamp": ts,
                    "date": date,
                    "price_usd": price,
                    "coint_id": self._coint_id,
                    "name": self._name,
                    "symbol": self._symbol,
                }
            )

        # Convertimos a DataFrame de Pandas
        df = pd.DataFrame(processed)

        # Ordenar por timestamp y quedarnos con el último registro por fecha
        df_sorted = df.sort_values(by=["date", "timestamp"])
        df_last_per_day = df_sorted.groupby("date", as_index=False).last()

        return self._sparksession.createDataFrame(
            df_last_per_day.drop(columns=["timestamp"])
        )
