class ArbitrageCalculator:
    """Calculates theoretical arbitrage opportunities after estimated fees."""

    def __init__(self, fee_rate=0.002):
        self.fee_rate = fee_rate

    def calculate(self, pair, market_data):
        valid_results = self._filter_valid_market_data(market_data)
        failed_results = self._filter_failed_market_data(market_data)

        if len(valid_results) < 2:
            return {
                "pair": pair,
                "error": "At least two valid exchange market results are required.",
                "checked_exchanges": valid_results,
                "failed_exchanges": failed_results,
            }

        lowest_buy = min(valid_results, key=lambda item: item["ask_price"])
        highest_sell = max(valid_results, key=lambda item: item["bid_price"])

        lowest_buy_price = lowest_buy["ask_price"]
        highest_sell_price = highest_sell["bid_price"]
        spread = highest_sell_price - lowest_buy_price
        estimated_fee = (lowest_buy_price + highest_sell_price) * self.fee_rate
        theoretical_profit = spread - estimated_fee

        return {
            "pair": pair,
            "lowest_buy_exchange": lowest_buy["exchange"],
            "lowest_buy_price": round(lowest_buy_price, 2),
            "highest_sell_exchange": highest_sell["exchange"],
            "highest_sell_price": round(highest_sell_price, 2),
            "spread": round(spread, 2),
            "estimated_fee": round(estimated_fee, 2),
            "theoretical_profit": round(theoretical_profit, 2),
            "profitable": theoretical_profit > 0,
            "same_exchange": lowest_buy["exchange"] == highest_sell["exchange"],
            "checked_exchanges": valid_results,
            "failed_exchanges": failed_results,
        }

    def _filter_valid_market_data(self, market_data):
        valid_results = []
        for result in market_data:
            if result.get("error"):
                continue
            if result.get("bid_price") is None or result.get("ask_price") is None:
                continue
            valid_results.append(result)
        return valid_results

    def _filter_failed_market_data(self, market_data):
        failed_results = []
        for result in market_data:
            if result.get("error"):
                failed_results.append(result)
            elif result.get("bid_price") is None or result.get("ask_price") is None:
                failed_copy = dict(result)
                failed_copy["error"] = "Bid or ask price was missing."
                failed_results.append(failed_copy)
        return failed_results
