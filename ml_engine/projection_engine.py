from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np


def _num(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@dataclass
class ProjectionResult:
    home_score: float
    away_score: float
    total: float
    spread_home: float
    spread_edge: float
    total_edge: float
    cover_prob_home: float
    cover_prob_away: float
    over_prob: float
    under_prob: float
    confidence: float
    recommended_spread_side: str
    recommended_total_side: str


def deterministic_projection(home_stats: Mapping[str, object], away_stats: Mapping[str, object]) -> tuple[float, float]:
    """Layer 1: possession + efficiency deterministic baseline."""
    off_home = _num(home_stats.get("OffEff"))
    off_away = _num(away_stats.get("OffEff"))
    def_home = _num(home_stats.get("DefEff"), 1.0)
    def_away = _num(away_stats.get("DefEff"), 1.0)

    pace_home = _num(home_stats.get("Pace"), 68.0)
    pace_away = _num(away_stats.get("Pace"), 68.0)
    avg_poss = (pace_home + pace_away) / 2.0

    # Turnover and rebounding effects
    tov_home = _num(home_stats.get("TOVPct"), 0.16)
    tov_away = _num(away_stats.get("TOVPct"), 0.16)
    oreb_home = _num(home_stats.get("OffRebPct"), 0.28)
    oreb_away = _num(away_stats.get("OffRebPct"), 0.28)

    poss_adj_home = avg_poss * (1 - tov_home) + avg_poss * oreb_home * 0.15
    poss_adj_away = avg_poss * (1 - tov_away) + avg_poss * oreb_away * 0.15
    poss = (poss_adj_home + poss_adj_away) / 2.0

    home_points = (off_home * (def_away / 100.0)) * (poss / 100.0)
    away_points = (off_away * (def_home / 100.0)) * (poss / 100.0)
    return home_points, away_points


def monte_carlo_layer(home_mean: float, away_mean: float, market_spread: float, market_total: float, sims: int = 12000, sigma: float = 11.5) -> dict[str, float]:
    """Layer 2: uncertainty modeling for spread and total probabilities."""
    rng = np.random.default_rng(42)
    sim_home = rng.normal(home_mean, sigma, sims)
    sim_away = rng.normal(away_mean, sigma, sims)

    sim_spread_home = sim_home - sim_away
    sim_total = sim_home + sim_away
    true_market_spread = -market_spread

    return {
        "cover_prob_home": float(np.mean(sim_spread_home > true_market_spread)),
        "cover_prob_away": float(np.mean(sim_spread_home < true_market_spread)),
        "over_prob": float(np.mean(sim_total > market_total)),
        "under_prob": float(np.mean(sim_total < market_total)),
    }


def situational_trend_adjustment(home_stats: Mapping[str, object], away_stats: Mapping[str, object]) -> tuple[float, float]:
    """Layer 3: market trend/situational adjustments (ATS and O/U proxies)."""
    home_adv = 1.75

    home_margin = _num(home_stats.get("AvgScoreMargin"), 0.0)
    away_margin = _num(away_stats.get("AvgScoreMargin"), 0.0)
    margin_adj = (home_margin - away_margin) * 0.08

    # O/U style signal proxy using pace + shooting profile
    pace_signal = (_num(home_stats.get("Pace"), 68.0) + _num(away_stats.get("Pace"), 68.0) - 136.0) * 0.15
    shooting_signal = (
        _num(home_stats.get("ThreePPct"), 0.33)
        + _num(away_stats.get("ThreePPct"), 0.33)
        - _num(home_stats.get("OppThreePPct"), 0.33)
        - _num(away_stats.get("OppThreePPct"), 0.33)
    ) * 8.0

    spread_shift = home_adv + margin_adj
    total_shift = pace_signal + shooting_signal
    return spread_shift, total_shift


def regression_rebalance(home_score: float, away_score: float, market_spread: float, market_total: float, ml_edge: float) -> tuple[float, float]:
    """Layer 4: regression-style shrinkage to market with ML override."""
    model_total = home_score + away_score
    model_spread = home_score - away_score

    market_implied_home = (market_total - market_spread) / 2.0
    market_implied_away = (market_total + market_spread) / 2.0

    # 70/30 blend baseline; ML edge amplifies model side when signal is strong.
    model_weight = float(np.clip(0.70 + ml_edge * 0.30, 0.50, 0.88))
    market_weight = 1.0 - model_weight

    blended_total = model_total * model_weight + market_total * market_weight
    blended_home = home_score * model_weight + market_implied_home * market_weight
    blended_away = away_score * model_weight + market_implied_away * market_weight

    # Final consistency pass so spread and total line up exactly.
    final_spread = model_spread * model_weight + (-market_spread) * market_weight
    final_home = (blended_total + final_spread) / 2.0
    final_away = (blended_total - final_spread) / 2.0
    return final_home, final_away


def run_five_layer_projection(
    home_team: str,
    away_team: str,
    home_stats: Mapping[str, object],
    away_stats: Mapping[str, object],
    market_spread: float,
    market_total: float,
    ml_edge: float,
    sims: int = 12000,
    sigma: float = 11.5,
) -> ProjectionResult:
    """Layer 5: unified projection output for score, probabilities, and recommendations."""
    base_home, base_away = deterministic_projection(home_stats, away_stats)

    spread_shift, total_shift = situational_trend_adjustment(home_stats, away_stats)
    shifted_home = base_home + (spread_shift / 2.0) + (total_shift / 2.0)
    shifted_away = base_away - (spread_shift / 2.0) + (total_shift / 2.0)

    final_home, final_away = regression_rebalance(
        home_score=shifted_home,
        away_score=shifted_away,
        market_spread=market_spread,
        market_total=market_total,
        ml_edge=ml_edge,
    )

    final_total = final_home + final_away
    final_spread = final_home - final_away
    true_market_spread = -market_spread

    spread_edge = final_spread - true_market_spread
    total_edge = final_total - market_total

    probs = monte_carlo_layer(
        home_mean=final_home,
        away_mean=final_away,
        market_spread=market_spread,
        market_total=market_total,
        sims=sims,
        sigma=sigma,
    )

    confidence = (max(probs["cover_prob_home"], probs["cover_prob_away"]) + max(probs["over_prob"], probs["under_prob"])) / 2.0

    spread_side = home_team if spread_edge > 0 else away_team
    total_side = "Over" if total_edge > 0 else "Under"

    return ProjectionResult(
        home_score=final_home,
        away_score=final_away,
        total=final_total,
        spread_home=final_spread,
        spread_edge=spread_edge,
        total_edge=total_edge,
        cover_prob_home=probs["cover_prob_home"],
        cover_prob_away=probs["cover_prob_away"],
        over_prob=probs["over_prob"],
        under_prob=probs["under_prob"],
        confidence=confidence,
        recommended_spread_side=spread_side,
        recommended_total_side=total_side,
    )
