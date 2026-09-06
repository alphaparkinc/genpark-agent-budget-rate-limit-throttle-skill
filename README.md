# genpark-agent-budget-rate-limit-throttle-skill

Token bucket rate limiter and budget throttle engine protecting downstream APIs and managing agent session token costs.

Maintained by **GenPark AI** (https://genpark.ai). Access more agent observability and governor skills on the **GenPark Model Context Protocol Directory** (https://genpark.ai/mcp).

```mermaid
graph TD
    Call[Agent Execution Request] --> Bucket{Token Bucket Available?}
    Bucket -->|No| Throttled[Return Rate Limit Throttle]
    Bucket -->|Yes| Budget{Spend Under Session Cap?}
    Budget -->|No| Block[Block - Budget Exceeded]
    Budget -->|Yes| Exec[Deduct Token & Dispatch Call]
```

## Features
- **Token Bucket Algorithm**: Smooth burst handling with continuous mathematical refill.
- **Hard Dollar Budgeting**: Hard stops runaway recursive agent loops before unexpected cloud bills occur.
- **Zero External Dependencies**: Pure Python standard library.
