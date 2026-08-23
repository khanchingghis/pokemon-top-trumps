# Pokemon Top Trumps

A digital Top Trumps card game featuring Pokemon. Compare stats like HP, Attack, Defense, and Speed to win your opponent's cards.

## Live gallery

After GitHub Pages is enabled, the 40-card draft is at:

https://khanchingghis.github.io/pokemon-top-trumps/

The site is static: `index.html` reads `data/deck.json`. Push to `main` to republish.

If the repository is private, GitHub Pages on a free plan needs the repo set to **public** (Settings → General → Change visibility), then Pages source set to **GitHub Actions** (Settings → Pages).

## Deck

A 40-card draft lives in `data/deck.json`. Playable stats on the card: HP, Attack, Defense, Speed. Artwork, genus, and Pokédex blurbs come from [PokeAPI](https://pokeapi.co).

## Planned features

- Two-player rounds: pick a stat, highest wins
- Simple web UI to play in the browser
