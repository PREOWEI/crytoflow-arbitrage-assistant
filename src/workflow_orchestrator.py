class WorkflowOrchestrator:
    """AI-assisted controller that decides and runs the analysis workflow."""

    def __init__(self, market_data_retriever, arbitrage_calculator, report_generator):
        self.market_data_retriever = market_data_retriever
        self.arbitrage_calculator = arbitrage_calculator
        self.report_generator = report_generator

    def run(self, nlp_output):
        if not nlp_output or nlp_output.get("status") != "success":
            return {
                "status": "error",
                "message": nlp_output.get("message", "NLP interpretation failed.") if nlp_output else "NLP interpretation failed.",
            }

        pair = nlp_output.get("pair")
        action = nlp_output.get("action")
        exchanges = nlp_output.get("exchanges", [])

        if not pair or action != "analyze" or not exchanges:
            return {
                "status": "error",
                "message": "Workflow cannot continue because required analysis data is missing.",
            }

        selected_exchanges = self._select_exchanges(exchanges)
        if len(selected_exchanges) < 2:
            return {
                "status": "error",
                "message": "At least two exchanges are required for arbitrage analysis.",
            }

        market_data = self.market_data_retriever.retrieve_market_data(pair, selected_exchanges)
        if not market_data:
            calculation_result = {
                "pair": pair,
                "error": "Market data could not be retrieved.",
            }
        else:
            calculation_result = self.arbitrage_calculator.calculate(pair, market_data)

        report = self.report_generator.generate(calculation_result)
        return {
            "status": "success",
            "pair": pair,
            "exchanges": selected_exchanges,
            "market_data": market_data,
            "calculation": calculation_result,
            "report": report,
        }

    def _select_exchanges(self, exchanges):
        """Agent decision point for choosing which exchanges should be queried."""
        unique_exchanges = []
        for exchange in exchanges:
            if exchange not in unique_exchanges:
                unique_exchanges.append(exchange)
        return unique_exchanges
