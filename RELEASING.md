# Releasing

The steps for the GitHub release are in the README, in the "Releasing" section. This
file covers the one step that CI cannot do: the claude.ai Design System page.

## Why this step is manual

The Bimble Design System page is a claude.ai artifact made from the "Design System"
Artifact type: <https://claude.ai/artifact/JyngCtzdycsq6LPFEp1pTj> (title "Bimble").
Its content is files under `project/`: `tokens.json`, `README.md`, the component
previews and the fonts. The logos are uploaded assets that `project/design-system.json`
lists.

A Claude session with the Artifact tool writes these files. The type's own
documentation (`artifact-type/reference/from-code.md` on that page) says that a sync
from GitHub uses "no scripts of ours, no API token". No documented way exists to
publish to the page from CI with a token in a repository secret. The release
workflow therefore stops after it attaches `bimble-design-system.zip` to the GitHub
release.

## Sync the Design System page after a release

Do this after the release workflow for `vX.Y.Z` finishes. Use one of the two routes.

### From Claude Code

1. Open Claude Code in a checkout of this repository on the `vX.Y.Z` tag.
2. Ask Claude: "Re-sync the Bimble design system
   https://claude.ai/artifact/JyngCtzdycsq6LPFEp1pTj from this repo at vX.Y.Z."
3. Claude reads the page back, merges the changes file by file and shows what
   changed. Approve the publish.

The files of `bimble-design-system.zip` from the release have the layout that the
page uses, so Claude can compare them with the page. To build the same files
locally with the right `meta.ref`, give the tag. On a tag checkout,
`make design-system` records `HEAD@<sha>` in place of the tag:

```bash
python3 scripts/build-design-system.py --ref "vX.Y.Z@$(git rev-parse --short HEAD)"
```

### From claude.ai

1. Make sure that a GitHub connector can read guilbep/bimble-design-skill.
2. Open the Bimble page and use "Sync from GitHub", or ask Claude on claude.ai:
   "Re-sync Bimble from GitHub at vX.Y.Z".

### After the sync

Open the page. Make sure that `tokens.json` shows `meta.ref` that starts with
`vX.Y.Z`, and that the index's `lastChange` names the same tag.
