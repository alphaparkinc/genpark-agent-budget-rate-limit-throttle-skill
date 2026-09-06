"""
Demonstration of genpark-agent-budget-rate-limit-throttle-skill
"""

from client import AgentBudgetRateLimiterClient

def main():
    limiter = AgentBudgetRateLimiterClient(requests_per_minute=120.0, max_budget_usd=0.01)

    print("Simulating agent requests with cost control...")
    for i in range(7):
        allowed, msg = limiter.acquire_call(cost_usd=0.002)
        print(f"Request {i+1}: Allowed={allowed} | {msg}")

    metrics = limiter.get_metrics()
    print("\n=== FINAL BUDGET METRICS ===")
    print(f"Spent: ${metrics['current_spent_usd']} / ${metrics['max_budget_usd']}")
    print(f"Remaining: ${metrics['budget_remaining_usd']}")

if __name__ == "__main__":
    main()
