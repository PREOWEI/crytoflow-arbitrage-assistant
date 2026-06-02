import time

import ccxt
import requests


class MarketDataRetriever:
    """Retrieves public market data using ccxt exchange tools."""

    def retrieve_market_data(self, pair, exchanges):
        results = []
        for exchange_name in exchanges:
            results.append(self._retrieve_from_exchange(pair, exchange_name))
        return results

    def _retrieve_from_exchange(self, pair, exchange_name):
        try:
            exchange_class = getattr(ccxt, exchange_name)
            exchange = exchange_class({"enableRateLimit": True, "timeout": 10000})
            ticker = exchange.fetch_ticker(pair)
            timestamp = ticker.get("timestamp")
            if timestamp and timestamp > 10000000000:
                timestamp = int(timestamp / 1000)

            return {
                "exchange": exchange_name,
                "pair": pair,
                "bid_price": ticker.get("bid"),
                "ask_price": ticker.get("ask"),
                "last_price": ticker.get("last"),
                "timestamp": timestamp or int(time.time()),
                "volume": ticker.get("baseVolume"),
            }
        except ccxt.BadSymbol:
            return self._error_result(exchange_name, pair, "Trading pair is not available on this exchange.")
        except ccxt.RequestTimeout:
            return self._error_result(exchange_name, pair, "Market data request timed out.")
        except ccxt.NetworkError:
            return self._error_result(exchange_name, pair, "Network error while retrieving market data.")
        except ccxt.ExchangeError:
            return self._error_result(exchange_name, pair, "Exchange error while retrieving market data.")
        except requests.exceptions.Timeout:
            return self._error_result(exchange_name, pair, "Supplementary data request timed out.")
        except requests.exceptions.RequestException:
            return self._error_result(exchange_name, pair, "Supplementary data request failed.")
        except Exception:
            return self._error_result(exchange_name, pair, "Market data could not be retrieved.")

    def get_supplementary_status(self):
        """Optional requests-based tool call for simple public connectivity status."""
        try:
            response = requests.get("https://api.coingecko.com/api/v3/ping", timeout=5)
            return {
                "status": "success",
                "status_code": response.status_code,
            }
        except requests.exceptions.Timeout as error:
            return {
                "status": "error",
                "message": str(error),
            }
        except requests.exceptions.RequestException as error:
            return {
                "status": "error",
                "message": str(error),
            }

    def _error_result(self, exchange_name, pair, message):
        return {
            "exchange": exchange_name,
            "pair": pair,
            "error": message,
        }
