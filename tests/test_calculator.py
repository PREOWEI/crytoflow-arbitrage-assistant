from src.arbitrage_calculator import ArbitrageCalculator


def sample_market_data():
    return [
        {
            "exchange": "binance",
            "pair": "BTC/USDT",
            "bid_price": 100.0,
            "ask_price": 101.0,
            "last_price": 100.5,
            "timestamp": 1715520000,
            "volume": 10,
        },
        {
            "exchange": "coinbase",
            "pair": "BTC/USDT",
            "bid_price": 110.0,
            "ask_price": 111.0,
            "last_price": 110.5,
            "timestamp": 1715520000,
            "volume": 12,
        },
    ]


def test_lowest_buy_detection():
    calculator = ArbitrageCalculator()
    result = calculator.calculate("BTC/USDT", sample_market_data())
    assert result["lowest_buy_exchange"] == "binance"
    assert result["lowest_buy_price"] == 101.0


def test_highest_sell_detection():
    calculator = ArbitrageCalculator()
    result = calculator.calculate("BTC/USDT", sample_market_data())
    assert result["highest_sell_exchange"] == "coinbase"
    assert result["highest_sell_price"] == 110.0


def test_spread_calculation():
    calculator = ArbitrageCalculator()
    result = calculator.calculate("BTC/USDT", sample_market_data())
    assert result["spread"] == 9.0


def test_estimated_fee_calculation():
    calculator = ArbitrageCalculator(fee_rate=0.002)
    result = calculator.calculate("BTC/USDT", sample_market_data())
    assert result["estimated_fee"] == 0.42


def test_theoretical_profit_calculation():
    calculator = ArbitrageCalculator(fee_rate=0.002)
    result = calculator.calculate("BTC/USDT", sample_market_data())
    assert result["theoretical_profit"] == 8.58
    assert result["profitable"] is True
    assert result["same_exchange"] is False


def test_not_enough_valid_exchange_data():
    calculator = ArbitrageCalculator()
    result = calculator.calculate("BTC/USDT", [sample_market_data()[0]])
    assert "error" in result
    assert len(result["checked_exchanges"]) == 1


def test_ignores_results_with_errors():
    calculator = ArbitrageCalculator()
    market_data = sample_market_data() + [{"exchange": "kraken", "pair": "BTC/USDT", "error": "failed"}]
    result = calculator.calculate("BTC/USDT", market_data)
    assert result["lowest_buy_exchange"] == "binance"
    assert result["highest_sell_exchange"] == "coinbase"
    assert len(result["checked_exchanges"]) == 2
    assert len(result["failed_exchanges"]) == 1


def test_ignores_results_with_none_bid_or_ask_prices():
    calculator = ArbitrageCalculator()
    market_data = sample_market_data() + [
        {"exchange": "kraken", "pair": "BTC/USDT", "bid_price": None, "ask_price": 90.0},
        {"exchange": "bitstamp", "pair": "BTC/USDT", "bid_price": 120.0, "ask_price": None},
    ]
    result = calculator.calculate("BTC/USDT", market_data)
    assert result["lowest_buy_exchange"] == "binance"
    assert result["highest_sell_exchange"] == "coinbase"
    assert len(result["checked_exchanges"]) == 2
    assert len(result["failed_exchanges"]) == 2


def test_same_exchange_is_returned_when_best_buy_and_sell_match():
    calculator = ArbitrageCalculator(fee_rate=0.002)
    market_data = [
        {
            "exchange": "binance",
            "pair": "BTC/USDT",
            "bid_price": 110.0,
            "ask_price": 101.0,
            "last_price": 105.0,
            "timestamp": 1715520000,
            "volume": 10,
        },
        {
            "exchange": "coinbase",
            "pair": "BTC/USDT",
            "bid_price": 100.0,
            "ask_price": 111.0,
            "last_price": 106.0,
            "timestamp": 1715520000,
            "volume": 12,
        },
    ]
    result = calculator.calculate("BTC/USDT", market_data)
    assert result["same_exchange"] is True
    assert result["checked_exchanges"] == market_data
