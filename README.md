# Pokemon Top Trumps

A digital Top Trumps card game featuring Pokemon. Compare stats like HP, Attack, Defence, Sp. Attack, Speed, Height, and Weight to win your opponent's cards.

## Live gallery

https://khanchingghis.github.io/pokemon-top-trumps/

30-card set (inset type bars, cinematic photos, folklore captions):

https://khanchingghis.github.io/pokemon-top-trumps/draft.html

Print files (PDF spec for a print shop):

https://khanchingghis.github.io/pokemon-top-trumps/print.html

Numbered card design options (photo backgrounds + typefaces):

https://khanchingghis.github.io/pokemon-top-trumps/designs.html

Balance sim (8,000 games each for 2 / 3 / 4 players):

https://khanchingghis.github.io/pokemon-top-trumps/simulate.html

The site is static: `index.html` and `draft.html` read `data/deck.json`. Locked look: folklore captions, cinematic type photos, inset type bars, pack key art backs. Push to `main` republishes.

One-time setup: Settings → Pages → Source → **GitHub Actions**. If the deploy is skipped, open Settings → Environments → **github-pages** and allow deployments from all branches.

## Deck

A 30-card pack of household names (mostly the original 151, plus Tyranitar and Lucario) lives in `data/deck.json`. Two players deal 15 each; three players deal 10 each. Playable stats: HP, Attack, Defence, Sp. Attack, Speed, Height, Weight. Artwork and Pokédex lines come from [PokeAPI](https://pokeapi.co).

## Planned features

- Two-player rounds: pick a stat, highest wins
- Simple web UI to play in the browser
