"""
MCP Server for Cascading Router Cost Quality Optimizer Skill.
"""

import json
import sys
from client import CascadingRouter

ROUTER = CascadingRouter()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "route_query",
                    "description": "Route agent query to optimal model tier based on complexity and SLA",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "prompt": {"type": "string"},
                            "quality_sla": {"type": "number", "default": 0.80},
                            "max_cost": {"type": "number"}
                        },
                        "required": ["prompt"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "route_query":
            res = ROUTER.route_query(
                args["prompt"],
                args.get("quality_sla", 0.80),
                args.get("max_cost")
            )
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
