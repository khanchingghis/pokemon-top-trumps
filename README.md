# Pokemon Top Trumps

A digital Top Trumps card game featuring Pokemon. Compare stats like HP, Attack, Defence, Sp. Attack, Speed, Height, and Weight to win your opponent's cards.

## Live gallery

https://khanchingghis.github.io/pokemon-top-trumps/

30-card set (inset type bars, cinematic photos, folklore captions):

https://khanchingghis.github.io/pokemon-top-trumps/draft.html

Print files (HTML + spec for a print shop). Cards are 62 × 100 mm:

https://khanchingghis.github.io/pokemon-top-trumps/print.html

30-card PDF (31 pages):

https://khanchingghis.github.io/pokemon-top-trumps/pokemon-top-trumps-30.pdf

40-card PDF (41 pages):

https://khanchingghis.github.io/pokemon-top-trumps/pokemon-top-trumps-40.pdf

40-card gallery:

https://khanchingghis.github.io/pokemon-top-trumps/index.html?set=40

Numbered card design options (photo backgrounds + typefaces):

https://khanchingghis.github.io/pokemon-top-trumps/designs.html

Balance sim (8,000 games each for 2 / 3 / 4 players):

https://khanchingghis.github.io/pokemon-top-trumps/simulate.html

The site is static: `index.html` and `draft.html` read `data/deck.json`. Locked look: folklore captions, cinematic type photos, inset type bars, pack key art backs. Push to `main` republishes.

One-time setup: Settings → Pages → Source → **GitHub Actions**. If the deploy is skipped, open Settings → Environments → **github-pages** and allow deployments from all branches.

## Deck

A 30-card pack lives in `data/deck.json` and a 40-card pack in `data/deck-40.json`. Cards print at official Winning Moves Top Trumps size: **62 × 100 mm** (the plastic case is 85 × 140 × 20 mm). Two players deal 15 each from the 30, or 20 each from the 40. Playable stats: HP, Attack, Defence, Sp. Attack, Speed, Height, Weight. Artwork and Pokédex lines come from [PokeAPI](https://pokeapi.co).

## Planned features

- Two-player rounds: pick a stat, highest wins
- Simple web UI to play in the browser
