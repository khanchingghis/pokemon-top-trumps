# Pokemon Top Trumps

A digital Top Trumps card game featuring Pokemon. Compare stats like HP, Attack, Defense, and Speed to win your opponent's cards.

## Live gallery

https://khanchingghis.github.io/pokemon-top-trumps/

Numbered card design options (photo backgrounds + typefaces):

https://khanchingghis.github.io/pokemon-top-trumps/designs.html

10-card draft (comic smash front, pack key art back):

https://khanchingghis.github.io/pokemon-top-trumps/draft.html

Balance sim (8,000 games each for 2 / 3 / 4 players):

https://khanchingghis.github.io/pokemon-top-trumps/simulate.html

The site is static: `index.html` reads `data/deck.json`. Playable stats: HP, Attack, Defense, Sp. Attack, Speed, Height, Weight. Art sits on a type-coloured field (HOME wash, Base Set texture, or Stage). `designs.html` is a numbered study of scene-photo backgrounds and layouts. Push to `main` republishes.

One-time setup: Settings → Pages → Source → **GitHub Actions**. If the deploy is skipped, open Settings → Environments → **github-pages** and allow deployments from all branches.

## Deck

A 40-card draft lives in `data/deck.json`. Playable stats on the card: HP, Attack, Defense, Sp. Attack, Speed, Height, Weight. Artwork, genus, and Pokédex blurbs come from [PokeAPI](https://pokeapi.co).

## Planned features

- Two-player rounds: pick a stat, highest wins
- Simple web UI to play in the browser
