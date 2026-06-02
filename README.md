# CrytoFlow Arbitrage Assistant

CrytoFlow Arbitrage Assistant is a command-line Python coursework project for educational cryptocurrency arbitrage analysis.

The system accepts a natural language request, detects the requested cryptocurrency pair and exchanges, retrieves public live market data, calculates a theoretical arbitrage result after estimated fees, and prints a beginner-friendly report.

This project does not execute real cryptocurrency trades. It is for educational and analytical purposes only.

## System Goal

The goal is to demonstrate a simple AI-assisted workflow for cryptocurrency market analysis:

1. Receive a user request.
2. Interpret natural language into structured workflow data.
3. Retrieve public market data using external tools.
4. Calculate theoretical arbitrage opportunities.
5. Generate a clear report for the user.

## AI / Agent Workflow

The project uses a lightweight agent-style workflow instead of a complex AI framework.

The `NaturalLanguageInterpreter` performs simple NLP using keyword extraction, pattern matching, intent recognition, exchange detection, and trading pair parsing.

The `WorkflowOrchestrator` acts as the agent/controller. It inspects the structured NLP output, checks whether the workflow can continue, decides which exchanges should be queried, triggers market data retrieval, runs the arbitrage calculation, and sends the result to the report generator.

## Tools and Libraries

- `ccxt` for public cryptocurrency exchange market data
- `requests` for optional supplementary public API access
- `python-dotenv` for environment configuration
- `pytest` for automated tests

No private API keys are required for the basic public data workflow.

## Project Structure

```text
CrytoFlow-Arbitrage-Assistant/
    main.py
    requirements.txt
    README.md
    .env.example

    src/
        __init__.py
        user_request_processor.py
        natural_language_interpreter.py
        workflow_orchestrator.py
        market_data_retriever.py
        arbitrage_calculator.py
        report_generator.py
        error_handler.py

    tests/
        __init__.py
        test_nlp.py
        test_calculator.py
        test_workflow.py
        test_report_generator.py
```

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install requirements:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` if you want to configure the estimated fee rate:

```bash
copy .env.example .env
```

Example configuration:

```text
FEE_RATE=0.002
```

`FEE_RATE=0.002` means the calculator estimates a 0.2 percent fee rate.

## How to Run

From the project folder, run:

```bash
python main.py
```

Example inputs:

```text
Check BTC arbitrage opportunities
Analyze ETH between Binance and Coinbase
Compare SOL between Kraken and Coinbase
```

## Example Output

```text
CrytoFlow Arbitrage Assistant
Educational analysis only. This tool does not execute trades.
Enter your cryptocurrency analysis request: Analyze ETH between Binance and Coinbase
Detected pair: ETH/USDT
Selected exchanges: binance, coinbase

Arbitrage Analysis Report
-------------------------
Analyzed pair: ETH/USDT
Checked Exchanges:

- binance
  Bid price: 1922.74
  Ask price: 1922.75
  Last price: 1922.75
  Volume: 100.5

- coinbase
  Bid price: 1921.8
  Ask price: 1923.1
  Last price: 1922.5
  Volume: 80.2

Lowest buy exchange: binance
Lowest buy price: 1922.75
Highest sell exchange: coinbase
Highest sell price: 1921.8
Estimated spread: -0.95
Estimated fees: 7.69
Theoretical profit: -8.64
Conclusion: No profitable arbitrage opportunity detected after estimated fees.

This report is for educational analysis only and does not execute trades.
```

If the best buy and best sell prices come from the same exchange, the report explains that no real cross-exchange arbitrage route was found.

## How to Run Tests

Run:

```bash
python -m pytest
```

The tests use mock data for workflow behavior and do not depend on live exchange APIs.

## Deployment Preparation

This repository is GitHub-ready:

- Source code is separated into `src/`.
- Tests are separated into `tests/`.
- Dependencies are listed in `requirements.txt`.
- Runtime configuration is documented in `.env.example`.
- The application runs from the command line with `python main.py`.

For deployment or submission, push the full folder to GitHub and include the README instructions for setup, execution, and testing.

## Safety Notice

CrytoFlow Arbitrage Assistant is not a trading bot. It does not place orders, access private wallets, or execute trades. Any arbitrage result is theoretical and depends on live data quality, exchange availability, fees, slippage, withdrawal costs, and market movement.
