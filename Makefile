# Bimble design skill: convenience targets. Python 3 and Node 20, no dependencies.

.DEFAULT_GOAL := help
.PHONY: help check skill design-system catalog dev

help:
	@echo "make check          check every contrast ratio the docs quote (exit 1 on a failure)"
	@echo "make skill          zip skills/bimble-design into dist/bimble-design.zip (+ .skill)"
	@echo "make design-system  build the claude.ai Design System files into dist/design-system/"
	@echo "make catalog        build the static catalog into site/"
	@echo "make dev            live catalog dev server (build + watch + live-reload) on :8080"
	@echo ""
	@echo "Tip: PORT=3000 make dev   to use a different port."

check:
	python3 scripts/check-contrast.py

# The skill as one archive: the bimble-design/ folder with SKILL.md at its root, which
# is what claude.ai, Claude Desktop and Codex install. The top folder must match the
# skill name, or claude.ai refuses the upload. A .skill file is the same zip.
skill:
	rm -rf dist && mkdir dist
	cd skills && zip -qr ../dist/bimble-design.zip bimble-design -x '*.DS_Store'
	cp dist/bimble-design.zip dist/bimble-design.skill

design-system:
	python3 scripts/build-design-system.py

catalog:
	node scripts/build-catalog.mjs

dev:
	node scripts/dev.mjs
