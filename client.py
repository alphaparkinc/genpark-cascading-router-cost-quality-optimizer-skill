"""
Cascading Router Cost Quality Optimizer Skill Client
Pure Python Standard Library implementation of LLM Cascading Router (Chen et al. FrugalGPT).
Scores incoming task complexity, queries model cost-performance profiles,
and selects the most cost-effective tier meeting required quality SLAs.
"""

import re
from typing import List, Dict, Any, Tuple, Optional


class CascadingRouter:
    """
    Model tier routing engine:
    Tier 1 (Nano/Small): Low cost, high speed (e.g., regex, simple extraction, format cleanup).
    Tier 2 (Flash/Medium): Moderate cost, strong general capabilities (e.g., summarization, standard code).
    Tier 3 (Pro/Large): Premium cost, deep reasoning (e.g., complex architecture, formal proofs, multi-step math).
    """

    MODEL_TIERS = {
        "tier_1_small": {"cost_per_million": 0.15, "quality_index": 0.65, "latency_ms": 200},
        "tier_2_medium": {"cost_per_million": 0.80, "quality_index": 0.85, "latency_ms": 500},
        "tier_3_large": {"cost_per_million": 5.00, "quality_index": 0.98, "latency_ms": 1500}
    }

    COMPLEXITY_KEYWORDS = {
        "tier_3_large": ["prove", "theorem", "architecture", "security audit", "byzantine", "concurrency", "distributed"],
        "tier_2_medium": ["summarize", "refactor", "explain", "review", "sql", "compare", "classify"],
        "tier_1_small": ["format", "json", "extract", "capitalize", "translate word", "count"]
    }

    def assess_complexity(self, prompt: str) -> Dict[str, Any]:
        """Assess semantic complexity score in range [0.0, 1.0]."""
        p_lower = prompt.lower()
        score = 0.3  # Base complexity

        # Keyword matching
        for kw in self.COMPLEXITY_KEYWORDS["tier_3_large"]:
            if kw in p_lower:
                score += 0.4
                break

        for kw in self.COMPLEXITY_KEYWORDS["tier_2_medium"]:
            if kw in p_lower:
                score += 0.2
                break

        # Length factor
        if len(prompt.split()) > 200:
            score += 0.2
        elif len(prompt.split()) < 20:
            score -= 0.1

        score = max(0.0, min(1.0, score))
        return {"complexity_score": round(score, 3)}

    def route_query(self, prompt: str, quality_sla: float = 0.80, max_cost: Optional[float] = None) -> Dict[str, Any]:
        """
        Select optimal model tier.
        """
        comp = self.assess_complexity(prompt)["complexity_score"]

        # Decision threshold based on complexity and SLA
        if comp >= 0.70 or quality_sla > 0.90:
            selected_tier = "tier_3_large"
        elif comp >= 0.40 or quality_sla > 0.70:
            selected_tier = "tier_2_medium"
        else:
            selected_tier = "tier_1_small"

        # Apply max_cost override constraint if provided
        if max_cost is not None:
            if selected_tier == "tier_3_large" and self.MODEL_TIERS["tier_3_large"]["cost_per_million"] > max_cost:
                selected_tier = "tier_2_medium"
            if selected_tier == "tier_2_medium" and self.MODEL_TIERS["tier_2_medium"]["cost_per_million"] > max_cost:
                selected_tier = "tier_1_small"

        tier_info = self.MODEL_TIERS[selected_tier]

        return {
            "selected_tier": selected_tier,
            "complexity_score": comp,
            "quality_sla": quality_sla,
            "estimated_cost_per_million": tier_info["cost_per_million"],
            "expected_quality": tier_info["quality_index"],
            "expected_latency_ms": tier_info["latency_ms"]
        }
