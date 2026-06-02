import os

from dotenv import load_dotenv

from src.arbitrage_calculator import ArbitrageCalculator
from src.market_data_retriever import MarketDataRetriever
from src.natural_language_interpreter import NaturalLanguageInterpreter
from src.report_generator import ReportGenerator
from src.user_request_processor import UserRequestProcessor
from src.workflow_orchestrator import WorkflowOrchestrator


def main():
    load_dotenv()

    fee_rate = float(os.getenv("FEE_RATE", "0.002"))

    interpreter = NaturalLanguageInterpreter()
    request_processor = UserRequestProcessor(interpreter)
    market_data_retriever = MarketDataRetriever()
    arbitrage_calculator = ArbitrageCalculator(fee_rate=fee_rate)
    report_generator = ReportGenerator()

    orchestrator = WorkflowOrchestrator(
        market_data_retriever=market_data_retriever,
        arbitrage_calculator=arbitrage_calculator,
        report_generator=report_generator,
    )

    print("CrytoFlow Arbitrage Assistant")
    print("Educational analysis only. This tool does not execute trades.")
    user_input = input("Enter your cryptocurrency analysis request: ")

    processed_request = request_processor.process_request(user_input)

    if processed_request.get("status") != "success":
        print(processed_request.get("message"))
        return

    structured_request = processed_request.get("data")
    print(f"Detected pair: {structured_request.get('pair')}")
    print(f"Selected exchanges: {', '.join(structured_request.get('exchanges', []))}")

    workflow_result = orchestrator.run(structured_request)
    print(workflow_result.get("report", workflow_result.get("message", "No report generated.")))


if __name__ == "__main__":
    main()
