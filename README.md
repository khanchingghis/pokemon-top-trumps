# Pokemon Top Trumps

A digital Top Trumps card game featuring Pokemon. Compare stats like HP, Attack, Defense, and Speed to win your opponent's cards.

## Live gallery

https://khanchingghis.github.io/pokemon-top-trumps/

The site is static: `index.html` reads `data/deck.json`. Every push (including this PR branch) republishes it.

One-time setup: Settings → Pages → Source → **GitHub Actions**. If the deploy is skipped, open Settings → Environments → **github-pages** and allow deployments from all branches.

## Deck

A 40-card draft lives in `data/deck.json`. Playable stats on the card: HP, Attack, Defense, Speed. Artwork, genus, and Pokédex blurbs come from [PokeAPI](https://pokeapi.co).

## Planned features

- Two-player rounds: pick a stat, highest wins
- Simple web UI to play in the browser
