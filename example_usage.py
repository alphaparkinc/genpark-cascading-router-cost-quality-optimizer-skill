"""
Example usage of Cascading Router Cost Quality Optimizer Skill.
"""

from client import CascadingRouter


def main():
    print("=== Cascading Router Cost Quality Optimizer Demonstration ===")
    router = CascadingRouter()

    queries = [
        ("Format this text into valid JSON payload", 0.70),
        ("Summarize the key differences between Postgres and MySQL", 0.80),
        ("Design a fault-tolerant Byzantine agreement protocol with dynamic quorums", 0.95),
        ("Quickly count the number of commas in this CSV row", 0.50)
    ]

    print("Evaluating Query Routing Optimization:\n")
    for prompt, sla in queries:
        res = router.route_query(prompt, quality_sla=sla)
        print(f"Prompt: '{prompt[:45]}...'")
        print(f"  Complexity: {res['complexity_score']} | SLA: {sla}")
        print(f"  -> Routed to: {res['selected_tier'].upper()}")
        print(f"  -> Cost: ${res['estimated_cost_per_million']}/M tokens | Latency: {res['expected_latency_ms']}ms\n")


if __name__ == "__main__":
    main()
