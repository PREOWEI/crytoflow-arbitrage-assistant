from src.report_generator import ReportGenerator


def test_report_includes_checked_exchanges():
    generator = ReportGenerator()
    report = generator.generate(
        {
            "pair": "ETH/USDT",
            "lowest_buy_exchange": "binance",
            "lowest_buy_price": 1922.75,
            "highest_sell_exchange": "coinbase",
            "highest_sell_price": 1924.0,
            "spread": 1.25,
            "estimated_fee": 7.69,
            "theoretical_profit": -6.44,
            "profitable": False,
            "same_exchange": False,
            "checked_exchanges": [
                {
                    "exchange": "binance",
                    "bid_price": 1922.74,
                    "ask_price": 1922.75,
                    "last_price": 1922.75,
                    "volume": 100.5,
                },
                {
                    "exchange": "coinbase",
                    "bid_price": 1921.8,
                    "ask_price": 1923.1,
                    "last_price": 1922.5,
                    "volume": 80.2,
                },
            ],
        }
    )

    assert "Analyzed pair: ETH/USDT" in report
    assert "Checked Exchanges:" in report
    assert "- binance" in report
    assert "Bid price: 1922.74" in report
    assert "- coinbase" in report
    assert "Ask price: 1923.1" in report


def test_same_exchange_report_has_clear_cross_exchange_message():
    generator = ReportGenerator()
    report = generator.generate(
        {
            "pair": "BTC/USDT",
            "lowest_buy_exchange": "binance",
            "lowest_buy_price": 101.0,
            "highest_sell_exchange": "binance",
            "highest_sell_price": 110.0,
            "spread": 9.0,
            "estimated_fee": 0.42,
            "theoretical_profit": 8.58,
            "profitable": True,
            "same_exchange": True,
            "checked_exchanges": [
                {
                    "exchange": "binance",
                    "bid_price": 110.0,
                    "ask_price": 101.0,
                    "last_price": 105.0,
                },
                {
                    "exchange": "coinbase",
                    "bid_price": 100.0,
                    "ask_price": 111.0,
                    "last_price": 106.0,
                },
            ],
        }
    )

    assert (
        "No cross-exchange arbitrage opportunity was found because the best buy "
        "and best sell prices came from the same exchange."
    ) in report


def test_report_includes_exchange_error_message():
    generator = ReportGenerator()
    report = generator.generate(
        {
            "pair": "SOL/USDT",
            "error": "At least two valid exchange market results are required.",
            "checked_exchanges": [],
            "failed_exchanges": [
                {
                    "exchange": "kraken",
                    "pair": "SOL/USDT",
                    "error": "Market data could not be retrieved.",
                }
            ],
        }
    )

    assert "- kraken" in report
    assert "Error: Market data could not be retrieved." in report
