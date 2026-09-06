"""
MCP Server for genpark-agent-budget-rate-limit-throttle-skill
Standard JSON-RPC 2.0 protocol over stdio.
"""

import sys
import json
from client import AgentBudgetRateLimiterClient

limiter = AgentBudgetRateLimiterClient()

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "check_rate_and_budget",
                        "description": "Verify rate quota and session budget availability.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "cost_usd": {"type": "number"}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "check_rate_and_budget":
            cost = args.get("cost_usd", 0.002)
            allowed, msg = limiter.acquire_call(cost_usd=cost)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"allowed": allowed, "message": msg, "metrics": limiter.get_metrics()})}]
                }
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
