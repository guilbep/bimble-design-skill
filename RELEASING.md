# Releasing

The steps for the GitHub release are in the README, in the "Releasing" section. This
file covers the one step that CI cannot do: the claude.ai Design System page.

## Why this step is manual

The Bimble Design System page lives on claude.ai, at
<https://claude.ai/artifact/JyngCtzdycsq6LPFEp1pTj> (title "Bimble"). No documented
way exists to publish to it from CI:

- Claude Code's `DesignSync` tool, which `/design-sync` uses, signs in with your
  claude.ai login or with `/design-login`. Every write needs a plan that you approve
  in the session. It has no token to store as a repository secret.
- No public API for Design System pages exists.

The release workflow therefore stops after it attaches `bimble-design-system.zip`
to the GitHub release.

## Sync the Design System page after a release

Do this after the release workflow for `vX.Y.Z` finishes.

1. Open a Claude Code session in this repository on the `vX.Y.Z` tag.
2. Run `make design-system`. It builds the files into `dist/design-system/project/`.
3. Run `/design-sync` and choose the "Bimble" design system.
4. Read the plan that it shows, then approve it.

Alternatively, open claude.ai and ask Claude: "re-sync Bimble from GitHub at vX.Y.Z".

After the sync, open the page and make sure that `tokens.json` shows `meta.ref`
equal to the new tag.
