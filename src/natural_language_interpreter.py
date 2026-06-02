import re

import ccxt


class NaturalLanguageInterpreter:
    """Simple NLP interpreter using keywords and pattern matching."""

    DEFAULT_EXCHANGES = ["binance", "kraken", "coinbase"]
    DEFAULT_MARKET_SOURCE = "binance"

    def __init__(self, auto_refresh=True):
        self.supported_exchanges = set(ccxt.exchanges)
        self.supported_pairs = set()
        if auto_refresh:
            self.refresh_supported_pairs()

    def refresh_supported_pairs(self):
        """Refresh supported trading pairs from a default public market source."""
        try:
            exchange_class = getattr(ccxt, self.DEFAULT_MARKET_SOURCE)
            exchange = exchange_class()
            markets = exchange.load_markets()
            self.supported_pairs = set(markets.keys())
        except Exception:
            # Fallback keeps the app usable if markets cannot be loaded at startup.
            self.supported_pairs = {"BTC/USDT", "ETH/USDT", "SOL/USDT"}
        return self.supported_pairs

    def interpret(self, user_input):
        text = user_input.lower()

        action = self._detect_action(text)
        exchanges = self._detect_exchanges(text)
        if exchanges is None:
            return {
                "status": "error",
                "message": "Unsupported exchange requested.",
            }

        pair = self._detect_pair(user_input)
        if pair is None:
            return {
                "status": "error",
                "message": "No cryptocurrency pair detected.",
            }

        if pair not in self.supported_pairs:
            return {
                "status": "error",
                "message": "Unsupported cryptocurrency pair requested.",
            }

        return {
            "status": "success",
            "pair": pair,
            "action": action,
            "exchanges": exchanges,
        }

    def _detect_action(self, text):
        action_keywords = ["analyze", "check", "compare", "find", "search", "arbitrage"]
        for keyword in action_keywords:
            if keyword in text:
                return "analyze"
        return "analyze"

    def _detect_exchanges(self, text):
        words = set(re.findall(r"[a-zA-Z0-9]+", text))
        detected = []
        unsupported_mentions = []

        for word in words:
            if word in self.supported_exchanges:
                detected.append(word)
            elif self._looks_like_exchange_name(word):
                unsupported_mentions.append(word)

        if unsupported_mentions:
            return None

        if not detected:
            return list(self.DEFAULT_EXCHANGES)

        return sorted(detected)

    def _looks_like_exchange_name(self, word):
        exchange_context_words = {
            "exchange",
            "exchanges",
            "platform",
            "market",
            "markets",
        }
        known_non_exchanges = {
            "analyze",
            "arbitrage",
            "between",
            "check",
            "coin",
            "compare",
            "crypto",
            "cryptocurrency",
            "find",
            "from",
            "opportunities",
            "opportunity",
            "request",
            "search",
            "the",
            "to",
        }
        return (word.endswith("exchange") or word in exchange_context_words) and word not in known_non_exchanges

    def _detect_pair(self, user_input):
        upper_text = user_input.upper()

        pair_match = re.search(r"\b([A-Z0-9]{2,10})\s*[/\-]\s*([A-Z0-9]{2,10})\b", upper_text)
        if pair_match:
            return f"{pair_match.group(1)}/{pair_match.group(2)}"

        compact_pair_match = re.search(r"\b([A-Z0-9]{2,10})(USDT|USD|EUR|BTC|ETH)\b", upper_text)
        if compact_pair_match:
            return f"{compact_pair_match.group(1)}/{compact_pair_match.group(2)}"

        symbols = self._extract_symbols_from_supported_pairs()
        words = re.findall(r"\b[A-Z0-9]{2,10}\b", upper_text)
        for word in words:
            if word in symbols:
                preferred_pair = f"{word}/USDT"
                if preferred_pair in self.supported_pairs:
                    return preferred_pair
                for pair in sorted(self.supported_pairs):
                    if pair.startswith(f"{word}/"):
                        return pair

        return None

    def _extract_symbols_from_supported_pairs(self):
        symbols = set()
        for pair in self.supported_pairs:
            if "/" in pair:
                symbols.add(pair.split("/")[0])
        return symbols
