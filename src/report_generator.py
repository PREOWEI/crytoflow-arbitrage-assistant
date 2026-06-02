class ReportGenerator:
    """Formats arbitrage calculation results into a readable report."""

    def generate(self, calculation_result):
        checked_exchange_section = self._format_checked_exchanges(
            calculation_result.get("checked_exchanges", []),
            calculation_result.get("failed_exchanges", []),
        )

        if calculation_result.get("error"):
            return (
                "Arbitrage Analysis Report\n"
                "-------------------------\n"
                f"Analyzed pair: {calculation_result.get('pair', 'Unknown')}\n"
                f"{checked_exchange_section}\n"
                f"Result: {calculation_result.get('error')}\n"
            )

        if calculation_result.get("same_exchange"):
            conclusion = (
                "No cross-exchange arbitrage opportunity was found because the best buy "
                "and best sell prices came from the same exchange."
            )
        elif calculation_result.get("profitable"):
            conclusion = "Potential cross-exchange arbitrage opportunity detected."
        else:
            conclusion = "No profitable arbitrage opportunity detected after estimated fees."

        return (
            "Arbitrage Analysis Report\n"
            "-------------------------\n"
            f"Analyzed pair: {calculation_result['pair']}\n"
            f"{checked_exchange_section}\n"
            f"Lowest buy exchange: {calculation_result['lowest_buy_exchange']}\n"
            f"Lowest buy price: {calculation_result['lowest_buy_price']}\n"
            f"Highest sell exchange: {calculation_result['highest_sell_exchange']}\n"
            f"Highest sell price: {calculation_result['highest_sell_price']}\n"
            f"Estimated spread: {calculation_result['spread']}\n"
            f"Estimated fees: {calculation_result['estimated_fee']}\n"
            f"Theoretical profit: {calculation_result['theoretical_profit']}\n"
            f"Conclusion: {conclusion}\n"
            "\n"
            "This report is for educational analysis only and does not execute trades."
        )

    def _format_checked_exchanges(self, checked_exchanges, failed_exchanges=None):
        failed_exchanges = failed_exchanges or []
        all_exchanges = checked_exchanges + failed_exchanges

        if not all_exchanges:
            return "Checked Exchanges:\nNo valid exchange market data was available.\n"

        lines = ["Checked Exchanges:"]
        for exchange_data in all_exchanges:
            lines.append("")
            lines.append(f"- {exchange_data.get('exchange', 'unknown')}")
            if exchange_data.get("error"):
                lines.append(f"  Error: {exchange_data.get('error')}")
                continue
            lines.append(f"  Bid price: {exchange_data.get('bid_price')}")
            lines.append(f"  Ask price: {exchange_data.get('ask_price')}")
            lines.append(f"  Last price: {exchange_data.get('last_price')}")
            if exchange_data.get("volume") is not None:
                lines.append(f"  Volume: {exchange_data.get('volume')}")

        return "\n".join(lines) + "\n"
