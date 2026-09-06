"""
Token Bucket Rate Limiter and Session Cost Budget Throttle.
Zero external dependencies, standard library only.
"""

import time
from typing import Dict, Any, Tuple

class AgentBudgetRateLimiterClient:
    """
    Regulates agent tool invocation frequency and monetary/token budget:
    - Token bucket rate limiting with automatic refill
    - Lifetime session dollar/token budget capping
    - Circuit breaker triggers when quota exceeded
    """

    def __init__(self, requests_per_minute: float = 60.0, max_budget_usd: float = 10.0):
        self.capacity = float(requests_per_minute)
        self.refill_rate = requests_per_minute / 60.0 # tokens per second
        self.tokens = self.capacity
        self.last_refill = time.time()

        self.max_budget_usd = max_budget_usd
        self.current_spent_usd = 0.0

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

    def acquire_call(self, cost_usd: float = 0.002) -> Tuple[bool, str]:
        """Checks rate limit tokens and spend budget before executing call."""
        self._refill()

        # Check spend budget
        if (self.current_spent_usd + cost_usd) > self.max_budget_usd:
            return False, f"BUDGET_EXCEEDED: spent ${self.current_spent_usd:.4f} exceeds limit of ${self.max_budget_usd:.2f}"

        # Check rate limit
        if self.tokens < 1.0:
            return False, "RATE_LIMIT_EXCEEDED: Token bucket empty, please throttle requests"

        self.tokens -= 1.0
        self.current_spent_usd += cost_usd
        return True, "ALLOWED"

    def get_metrics(self) -> Dict[str, Any]:
        """Returns current rate limiter and spend statistics."""
        self._refill()
        return {
            "available_rate_tokens": round(self.tokens, 2),
            "current_spent_usd": round(self.current_spent_usd, 4),
            "max_budget_usd": self.max_budget_usd,
            "budget_remaining_usd": round(self.max_budget_usd - self.current_spent_usd, 4)
        }
