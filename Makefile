.PHONY: fmt test-fmt makedocs run hooks sprite-export sprite-build pal-commonizer pallet-maker commit

fmt:
	uv run python -B scripts/formatter/formatter.py

test-fmt:
	uv run python -B -m unittest discover -s scripts -p 'test_*.py'

makedocs:
	uv run python -B scripts/docs-index/docs_index.py

run:
	$(MAKE) fmt
	$(MAKE) test-fmt
	$(MAKE) makedocs

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

commit: # sync to git
	git pull origin main
	git add --all
	if ! git diff --cached --quiet; then \
		git commit -m 'update'; \
		git push origin main ; \
	else \
		echo "no changes." ; \
	fi
