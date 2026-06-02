from src.natural_language_interpreter import NaturalLanguageInterpreter


def make_interpreter():
    interpreter = NaturalLanguageInterpreter(auto_refresh=False)
    interpreter.supported_pairs = {"BTC/USDT", "ETH/USDT", "SOL/USDT", "ADA/USDT"}
    interpreter.supported_exchanges = {"binance", "kraken", "coinbase"}
    return interpreter


def test_btc_request_detection():
    interpreter = make_interpreter()
    result = interpreter.interpret("Check BTC arbitrage opportunities")
    assert result["status"] == "success"
    assert result["pair"] == "BTC/USDT"


def test_eth_request_detection():
    interpreter = make_interpreter()
    result = interpreter.interpret("Analyze ETH between Binance and Coinbase")
    assert result["status"] == "success"
    assert result["pair"] == "ETH/USDT"
    assert result["exchanges"] == ["binance", "coinbase"]


def test_sol_request_detection():
    interpreter = make_interpreter()
    result = interpreter.interpret("Compare SOL between Kraken and Coinbase")
    assert result["status"] == "success"
    assert result["pair"] == "SOL/USDT"
    assert result["exchanges"] == ["coinbase", "kraken"]


def test_exchange_detection():
    interpreter = make_interpreter()
    result = interpreter.interpret("Compare SOL between Kraken and Coinbase")
    assert result["exchanges"] == ["coinbase", "kraken"]


def test_default_exchanges_when_none_are_specified():
    interpreter = make_interpreter()
    result = interpreter.interpret("Check BTC arbitrage opportunities")
    assert result["exchanges"] == ["binance", "kraken", "coinbase"]


def test_action_detection():
    interpreter = make_interpreter()
    result = interpreter.interpret("Compare ETH prices")
    assert result["action"] == "analyze"


def test_invalid_request_with_no_pair():
    interpreter = make_interpreter()
    result = interpreter.interpret("Find arbitrage opportunities")
    assert result["status"] == "error"
    assert result["message"] == "No cryptocurrency pair detected."


def test_unsupported_exchange_handling():
    interpreter = make_interpreter()
    result = interpreter.interpret("Analyze BTC on Fakeexchange")
    assert result["status"] == "error"
    assert result["message"] == "Unsupported exchange requested."
