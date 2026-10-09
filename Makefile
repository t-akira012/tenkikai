ZIP_ROOT=tenkikai
ZIP_OUTPUT=dist/tenkikai.zip
ZIP_RUNTIME_FILES= \
	tenkikai.def \
	cns/command.cmd \
	cns/constants.cns \
	cns/state.cns \
	cns/observ.cns \
	cns/helper.cns \
	cns/common1.cns \
	cns/anim.air \
	binary/sprite.sff \
	binary/sound.snd \
	binary/pal1.act

.PHONY: fmt fmt-check test-fmt makedocs makedocs-check run check hooks sprite-export sprite-build pal-commonizer pallet-maker zip commit

fmt:
	uv run python -B scripts/formatter/formatter.py

fmt-check:
	uv run python -B scripts/formatter/formatter.py --check

test-fmt:
	uv run python -B -m unittest discover -s scripts -p 'test_*.py'

makedocs:
	uv run python -B scripts/docs-index/docs_index.py

makedocs-check:
	uv run python -B scripts/docs-index/docs_index.py --check

run:
	$(MAKE) fmt
	$(MAKE) test-fmt
	$(MAKE) makedocs

check:
	$(MAKE) fmt-check
	$(MAKE) test-fmt
	$(MAKE) makedocs-check

hooks:
	git config core.hooksPath .githooks

sprite-export:
	uv run python -B scripts/sprite-editor/sprite_editor.py sff-to-json \
		--input binary/sprite.sff \
		--output-json dist/sprite.json \
		--output-png dist/sprites/

sprite-build:
	uv run python -B scripts/sprite-editor/sprite_editor.py json-to-sff \
		--input-json assets/sprite.json \
		--input-png assets/sprites/ \
		--output binary/sprite.sff

pal-commonizer:
	uv run python -B scripts/palette-commonizer/palette_commonizer.py \
		--palette binary/pal1.act \
		--input assets/sprites/ \
		--output dist/pallet-commonizer/ \
		--overwrite

pallet-maker:
	uv run python -B scripts/pallet-maker/pallet_maker.py \
		--input assets/sprites/ \
		--output binary/pal1.act

zip:
	mkdir -p dist
	rm -f "$(ZIP_OUTPUT)"
	cd .. && zip -9 "$(ZIP_ROOT)/$(ZIP_OUTPUT)" $(addprefix $(ZIP_ROOT)/,$(ZIP_RUNTIME_FILES))

commit: # sync to git
	git pull origin main
	git add --all
	if ! git diff --cached --quiet; then \
		git commit -m 'update'; \
		git push origin main ; \
	else \
		echo "no changes." ; \
	fi
