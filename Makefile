.PHONY: fmt test-fmt commit

fmt:
	uv run python -B scripts/formatter.py

test-fmt:
	uv run python -B -m unittest discover -s scripts -p 'test_*.py'

commit: # sync to git
	git pull origin main
	git add --all
	if ! git diff --cached --quiet; then \
		git commit -m 'update'; \
		git push origin main ; \
	else \
		echo "no changes." ; \
	fi
