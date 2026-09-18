.PHONY: fmt test-fmt sprite-export sprite-build commit

fmt:
	uv run python -B scripts/formatter/formatter.py

test-fmt:
	uv run python -B -m unittest discover -s scripts -p 'test_*.py'

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

commit: # sync to git
	git pull origin main
	git add --all
	if ! git diff --cached --quiet; then \
		git commit -m 'update'; \
		git push origin main ; \
	else \
		echo "no changes." ; \
	fi
