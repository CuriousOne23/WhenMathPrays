## wordnet_raw local files

These `data.*` and `index.*` files are not kept in Git and should remain as full local copies on the developer machine.

Upstream source: Princeton WordNet download page
https://wordnet.princeton.edu/download

Expected local filenames include `data.noun`, `data.verb`, `data.adj`, `data.adv`, and matching `index.*` files.

Future CI/docs samples can be added under a different filename pattern; do not commit full dumps.

## Ignored local files

These paths are listed in the repo-root .gitignore and stay local in this working tree:

- data.noun, data.verb, data.adj, data.adv
- index.noun, index.verb, index.adj, index.sense
- any data.* or index.* dump in this folder
- any *.full file in this folder

These dumps are not on GitHub. Full WordNet lives on the developer machine.
Upstream source: https://wordnet.princeton.edu/download

Still tracked in this folder:

- README.md
- *.exc
- frames.vrb
- sents.vrb
- sentidx.vrb

Later samples can use a different filename, for example data.noun.sample, not data.noun.

