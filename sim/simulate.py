#!/usr/bin/env python3
"""Simulate Top Trumps games for deck balance analysis."""

from __future__ import annotations

import json
import math
import random
import statistics
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECK_PATH = ROOT / "data" / "deck.json"
OUT_PATH = ROOT / "data" / "sim-results.json"

STAT_IDS = [
    "hp",
    "attack",
    "defense",
    "special_attack",
    "speed",
    "height_m",
    "weight_kg",
]
STAT_LABELS = {
    "hp": "HP",
    "attack": "Attack",
    "defense": "Defense",
    "special_attack": "Sp. Attack",
    "speed": "Speed",
    "height_m": "Height",
    "weight_kg": "Weight",
}

GAMES = 8000
MAX_ROUNDS = 2500
SEED = 42


def percentile_map(cards: list[dict]) -> dict[str, dict[str, float]]:
    """card slug -> stat -> percentile in [0, 1] vs the full deck."""
    n = len(cards)
    out = {c["slug"]: {} for c in cards}
    for stat in STAT_IDS:
        vals = [c["stats"][stat] for c in cards]
        for card in cards:
            v = card["stats"][stat]
            below = sum(1 for x in vals if x < v)
            out[card["slug"]][stat] = below / (n - 1)
    return out


def z_map(cards: list[dict]) -> dict[str, dict[str, float]]:
    out = {c["slug"]: {} for c in cards}
    for stat in STAT_IDS:
        vals = [c["stats"][stat] for c in cards]
        mean = statistics.fmean(vals)
        stdev = statistics.pstdev(vals) or 1.0
        for card in cards:
            out[card["slug"]][stat] = (card["stats"][stat] - mean) / stdev
    return out


def pick_stat(card: dict, pct: dict, z: dict) -> str:
    slug = card["slug"]
    best = STAT_IDS[0]
    best_key = (-1.0, -999.0)
    for stat in STAT_IDS:
        key = (pct[slug][stat], z[slug][stat])
        if key > best_key:
            best_key = key
            best = stat
    return best


def deal(cards: list[dict], n_players: int, rng: random.Random) -> list[deque]:
    shuffled = list(cards)
    rng.shuffle(shuffled)
    usable = len(shuffled) - (len(shuffled) % n_players)
    shuffled = shuffled[:usable]
    hands = [deque() for _ in range(n_players)]
    for i, card in enumerate(shuffled):
        hands[i % n_players].append(card)
    return hands


def next_with_cards(hands: list[deque], start: int) -> int | None:
    n = len(hands)
    for step in range(n):
        i = (start + step) % n
        if hands[i]:
            return i
    return None


def summarize(values: list[int]) -> dict:
    if not values:
        return {"n": 0}
    ordered = sorted(values)

    def pct(p: float) -> float:
        if len(ordered) == 1:
            return float(ordered[0])
        k = (len(ordered) - 1) * p
        lo = math.floor(k)
        hi = math.ceil(k)
        if lo == hi:
            return float(ordered[lo])
        return ordered[lo] * (hi - k) + ordered[hi] * (k - lo)

    return {
        "n": len(ordered),
        "mean": round(statistics.fmean(ordered), 2),
        "median": statistics.median(ordered),
        "p10": round(pct(0.10), 1),
        "p25": round(pct(0.25), 1),
        "p75": round(pct(0.75), 1),
        "p90": round(pct(0.90), 1),
        "min": ordered[0],
        "max": ordered[-1],
    }


def histogram(values: list[int], edges: list[int]) -> dict[str, int]:
    counts = [0] * (len(edges) - 1)
    for v in values:
        placed = False
        for i in range(len(edges) - 1):
            lo, hi = edges[i], edges[i + 1]
            if (v >= lo) and (v < hi or (i == len(edges) - 2 and v <= hi)):
                counts[i] += 1
                placed = True
                break
        if not placed:
            counts[-1] += 1
    labels = []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        if i == len(edges) - 2:
            labels.append(f"{lo}–{hi}")
        else:
            labels.append(f"{lo}–{hi - 1}")
    return {"labels": labels, "counts": counts}


def play_game(cards, n_players, pct, z, rng) -> dict:
    hands = deal(cards, n_players, rng)
    pot: list[dict] = []
    chooser = 0
    rounds = 0
    ties = 0
    first_elim_round = None
    pick_counts = Counter()
    pick_wins = Counter()
    card_round_wins = Counter()

    while rounds < MAX_ROUNDS:
        alive = [i for i, h in enumerate(hands) if h]
        if len(alive) <= 1:
            winner = alive[0] if alive else 0
            return {
                "finished": True,
                "rounds": rounds,
                "ties": ties,
                "winner": winner,
                "first_elim_round": first_elim_round,
                "pick_counts": pick_counts,
                "pick_wins": pick_wins,
                "card_round_wins": card_round_wins,
            }

        if not hands[chooser]:
            nxt = next_with_cards(hands, chooser)
            if nxt is None:
                break
            chooser = nxt
            continue

        rounds += 1
        chooser_card = hands[chooser][0]
        stat = pick_stat(chooser_card, pct, z)
        pick_counts[stat] += 1

        played: list[tuple[int, dict]] = []
        for i in alive:
            played.append((i, hands[i].popleft()))

        max_v = max(c["stats"][stat] for _, c in played)
        winners = [i for i, c in played if c["stats"][stat] == max_v]
        for _, c in played:
            pot.append(c)
        if len(winners) == 1:
            w = winners[0]
            pick_wins[stat] += 1
            rng.shuffle(pot)
            hands[w].extend(pot)
            pot = []
            for i, c in played:
                if c["stats"][stat] == max_v:
                    card_round_wins[c["slug"]] += 1
            chooser = w
        else:
            ties += 1
            if not hands[chooser]:
                nxt = next_with_cards(hands, chooser + 1)
                if nxt is not None:
                    chooser = nxt

        remaining = sum(1 for h in hands if h)
        if first_elim_round is None and remaining < n_players and remaining > 1:
            first_elim_round = rounds

    return {
        "finished": False,
        "rounds": rounds,
        "ties": ties,
        "winner": None,
        "first_elim_round": first_elim_round,
        "pick_counts": pick_counts,
        "pick_wins": pick_wins,
        "card_round_wins": card_round_wins,
    }


def run_player_count(cards, n_players, pct, z, games, seed) -> dict:
    rng = random.Random(seed + n_players * 1009)
    rounds = []
    ties = []
    unfinished = 0
    seat_wins = Counter()
    first_elim = []
    pick_counts = Counter()
    pick_wins = Counter()
    card_round_wins = Counter()

    for _ in range(games):
        result = play_game(cards, n_players, pct, z, rng)
        pick_counts.update(result["pick_counts"])
        pick_wins.update(result["pick_wins"])
        card_round_wins.update(result["card_round_wins"])
        if not result["finished"]:
            unfinished += 1
            continue
        rounds.append(result["rounds"])
        ties.append(result["ties"])
        seat_wins[result["winner"]] += 1
        if result["first_elim_round"] is not None:
            first_elim.append(result["first_elim_round"])

    finished = len(rounds)
    total_picks = sum(pick_counts.values()) or 1
    stats_used = []
    for stat in STAT_IDS:
        chosen = pick_counts[stat]
        wins = pick_wins[stat]
        stats_used.append(
            {
                "id": stat,
                "label": STAT_LABELS[stat],
                "chosen": chosen,
                "chosen_pct": round(100 * chosen / total_picks, 2),
                "win_when_chosen_pct": round(100 * wins / chosen, 2) if chosen else 0.0,
            }
        )

    slug_name = {c["slug"]: c["name"] for c in cards}
    top_cards = [
        {"slug": slug, "name": slug_name[slug], "round_wins": wins}
        for slug, wins in card_round_wins.most_common(12)
    ]

    edges = [0, 20, 40, 60, 80, 100, 150, 200, 300, 500, 1000, MAX_ROUNDS]
    seat = [{"seat": i, "wins": seat_wins[i], "win_pct": round(100 * seat_wins[i] / finished, 2) if finished else 0} for i in range(n_players)]

    return {
        "players": n_players,
        "games": games,
        "finished": finished,
        "unfinished": unfinished,
        "cards_dealt_each": (len(cards) // n_players),
        "rounds": summarize(rounds),
        "ties": summarize(ties),
        "first_elimination_round": summarize(first_elim) if n_players > 2 else None,
        "round_histogram": histogram(rounds, edges),
        "seat_wins": seat,
        "first_player_win_pct": seat[0]["win_pct"] if seat else 0,
        "fair_share_pct": round(100 / n_players, 2),
        "stats_chosen": stats_used,
        "top_round_winning_cards": top_cards,
    }


def main() -> None:
    deck = json.loads(DECK_PATH.read_text())
    cards = deck["cards"]
    pct = percentile_map(cards)
    z = z_map(cards)
    results = {
        "meta": {
            "games_per_count": GAMES,
            "max_rounds": MAX_ROUNDS,
            "seed": SEED,
            "strategy": "Pick the stat with the highest full-deck percentile on the chooser's card (z-score tie-break). Winner of a round shuffles the won cards onto the bottom of their deck. Ties go to a pot for the next unique winner. 30-card pack: 2p=15, 3p=10, 4p=7 (2 unused).",
            "stats": [STAT_LABELS[s] for s in STAT_IDS],
        },
        "by_players": {},
    }
    for n in (2, 3, 4):
        print(f"simulating {GAMES} games with {n} players…")
        results["by_players"][str(n)] = run_player_count(cards, n, pct, z, GAMES, SEED)
        r = results["by_players"][str(n)]["rounds"]
        print(f"  median rounds {r['median']}, mean {r['mean']}, unfinished {results['by_players'][str(n)]['unfinished']}")

    OUT_PATH.write_text(json.dumps(results, indent=2) + "\n")
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    main()
