/* Top Trumps engine — keep in sync with sim/simulate.py */
export const STAT_IDS = [
  "hp",
  "attack",
  "defense",
  "special_attack",
  "speed",
  "height_m",
  "weight_kg",
];

export const STAT_LABELS = {
  hp: "HP",
  attack: "Attack",
  defense: "Defense",
  special_attack: "Sp. Attack",
  speed: "Speed",
  height_m: "Height",
  weight_kg: "Weight",
};

const MAX_ROUNDS = 2500;

function percentileMap(cards) {
  const n = cards.length;
  const out = {};
  for (const c of cards) out[c.slug] = {};
  for (const stat of STAT_IDS) {
    const vals = cards.map((c) => c.stats[stat]);
    for (const card of cards) {
      const v = card.stats[stat];
      let below = 0;
      for (const x of vals) if (x < v) below += 1;
      out[card.slug][stat] = below / (n - 1);
    }
  }
  return out;
}

function zMap(cards) {
  const out = {};
  for (const c of cards) out[c.slug] = {};
  for (const stat of STAT_IDS) {
    const vals = cards.map((c) => c.stats[stat]);
    const mean = vals.reduce((a, b) => a + b, 0) / vals.length;
    const varSum = vals.reduce((a, b) => a + (b - mean) ** 2, 0) / vals.length;
    const stdev = Math.sqrt(varSum) || 1;
    for (const card of cards) {
      out[card.slug][stat] = (card.stats[stat] - mean) / stdev;
    }
  }
  return out;
}

function pickStat(card, pct, z) {
  let best = STAT_IDS[0];
  let bestP = -1;
  let bestZ = -999;
  for (const stat of STAT_IDS) {
    const p = pct[card.slug][stat];
    const zv = z[card.slug][stat];
    if (p > bestP || (p === bestP && zv > bestZ)) {
      bestP = p;
      bestZ = zv;
      best = stat;
    }
  }
  return best;
}

function mulberry32(seed) {
  let a = seed >>> 0;
  return function rng() {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(arr, rng) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function deal(cards, nPlayers, rng) {
  const shuffled = shuffle(cards.slice(), rng);
  const usable = shuffled.length - (shuffled.length % nPlayers);
  const hands = Array.from({ length: nPlayers }, () => []);
  for (let i = 0; i < usable; i++) hands[i % nPlayers].push(shuffled[i]);
  return hands;
}

function nextWithCards(hands, start) {
  const n = hands.length;
  for (let step = 0; step < n; step++) {
    const i = (start + step) % n;
    if (hands[i].length) return i;
  }
  return null;
}

function playGame(cards, nPlayers, pct, z, rng) {
  const hands = deal(cards, nPlayers, rng);
  let pot = [];
  let chooser = 0;
  let rounds = 0;
  let ties = 0;
  let firstElim = null;
  const pickCounts = {};
  const pickWins = {};
  for (const s of STAT_IDS) {
    pickCounts[s] = 0;
    pickWins[s] = 0;
  }

  while (rounds < MAX_ROUNDS) {
    const alive = [];
    for (let i = 0; i < nPlayers; i++) if (hands[i].length) alive.push(i);
    if (alive.length <= 1) {
      return { finished: true, rounds, ties, winner: alive[0] ?? 0, firstElim };
    }
    if (!hands[chooser].length) {
      const nxt = nextWithCards(hands, chooser);
      if (nxt == null) break;
      chooser = nxt;
      continue;
    }

    rounds += 1;
    const stat = pickStat(hands[chooser][0], pct, z);
    pickCounts[stat] += 1;

    const played = alive.map((i) => [i, hands[i].shift()]);
    let maxV = -Infinity;
    for (const [, c] of played) maxV = Math.max(maxV, c.stats[stat]);
    const winners = played.filter(([, c]) => c.stats[stat] === maxV).map(([i]) => i);
    for (const [, c] of played) pot.push(c);

    if (winners.length === 1) {
      const w = winners[0];
      pickWins[stat] += 1;
      shuffle(pot, rng);
      hands[w].push(...pot);
      pot = [];
      chooser = w;
    } else {
      ties += 1;
      if (!hands[chooser].length) {
        const nxt = nextWithCards(hands, chooser + 1);
        if (nxt != null) chooser = nxt;
      }
    }

    if (firstElim == null) {
      let remaining = 0;
      for (const h of hands) if (h.length) remaining += 1;
      if (remaining < nPlayers && remaining > 1) firstElim = rounds;
    }
  }
  return { finished: false, rounds, ties, winner: null, firstElim };
}

function median(values) {
  if (!values.length) return 0;
  const o = values.slice().sort((a, b) => a - b);
  const m = Math.floor(o.length / 2);
  return o.length % 2 ? o[m] : (o[m - 1] + o[m]) / 2;
}

function mean(values) {
  if (!values.length) return 0;
  return values.reduce((a, b) => a + b, 0) / values.length;
}

export function simulate(cards, nPlayers, games, seed) {
  const pct = percentileMap(cards);
  const z = zMap(cards);
  const rng = mulberry32(seed);
  const rounds = [];
  const ties = [];
  const firstElim = [];
  let unfinished = 0;
  const seatWins = Array(nPlayers).fill(0);

  for (let g = 0; g < games; g++) {
    const r = playGame(cards, nPlayers, pct, z, rng);
    if (!r.finished) {
      unfinished += 1;
      continue;
    }
    rounds.push(r.rounds);
    ties.push(r.ties);
    seatWins[r.winner] += 1;
    if (r.firstElim != null) firstElim.push(r.firstElim);
  }

  const finished = rounds.length;
  return {
    players: nPlayers,
    games,
    finished,
    unfinished,
    rounds: {
      mean: mean(rounds),
      median: median(rounds),
      min: rounds.length ? Math.min(...rounds) : 0,
      max: rounds.length ? Math.max(...rounds) : 0,
    },
    ties: { mean: mean(ties), median: median(ties) },
    firstElim: firstElim.length
      ? { mean: mean(firstElim), median: median(firstElim) }
      : null,
    firstPlayerWinPct: finished ? (100 * seatWins[0]) / finished : 0,
    seatWins,
  };
}
