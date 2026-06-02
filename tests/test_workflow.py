from src.workflow_orchestrator import WorkflowOrchestrator


class MockMarketDataRetriever:
    def __init__(self, data):
        self.data = data

    def retrieve_market_data(self, pair, exchanges):
        return self.data


class MockCalculator:
    def __init__(self, result):
        self.result = result

    def calculate(self, pair, market_data):
        return self.result


class MockReportGenerator:
    def generate(self, calculation_result):
        if calculation_result.get("error"):
            return f"Error report: {calculation_result['error']}"
        return "Generated arbitrage report"


def test_full_workflow_success():
    market_data = [
        {"exchange": "binance", "bid_price": 100.0, "ask_price": 101.0},
        {"exchange": "coinbase", "bid_price": 110.0, "ask_price": 111.0},
    ]
    calculation = {"pair": "BTC/USDT", "profitable": True}
    orchestrator = WorkflowOrchestrator(
        MockMarketDataRetriever(market_data),
        MockCalculator(calculation),
        MockReportGenerator(),
    )

    result = orchestrator.run(
        {
            "status": "success",
            "pair": "BTC/USDT",
            "action": "analyze",
            "exchanges": ["binance", "coinbase"],
        }
    )

    assert result["status"] == "success"
    assert result["report"] == "Generated arbitrage report"


def test_invalid_nlp_output_stops_workflow():
    orchestrator = WorkflowOrchestrator(
        MockMarketDataRetriever([]),
        MockCalculator({}),
        MockReportGenerator(),
    )
    result = orchestrator.run({"status": "error", "message": "No cryptocurrency pair detected."})
    assert result["status"] == "error"
    assert result["message"] == "No cryptocurrency pair detected."


def test_market_data_retrieval_failure_returns_error():
    orchestrator = WorkflowOrchestrator(
        MockMarketDataRetriever([]),
        MockCalculator({}),
        MockReportGenerator(),
    )
    result = orchestrator.run(
        {
            "status": "success",
            "pair": "BTC/USDT",
            "action": "analyze",
            "exchanges": ["binance", "coinbase"],
        }
    )
    assert result["status"] == "success"
    assert result["calculation"]["error"] == "Market data could not be retrieved."
    assert result["report"] == "Error report: Market data could not be retrieved."


def test_report_is_generated_correctly():
    calculation = {"pair": "ETH/USDT", "profitable": False}
    orchestrator = WorkflowOrchestrator(
        MockMarketDataRetriever([{"exchange": "binance"}, {"exchange": "coinbase"}]),
        MockCalculator(calculation),
        MockReportGenerator(),
    )
    result = orchestrator.run(
        {
            "status": "success",
            "pair": "ETH/USDT",
            "action": "analyze",
            "exchanges": ["binance", "coinbase"],
        }
    )
    assert result["report"] == "Generated arbitrage report"
