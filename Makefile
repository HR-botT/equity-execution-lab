.PHONY: install test lint format clean run-normal

install:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

lint:
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/
	isort src/ tests/

clean:
	rm -rf .pytest_cache .coverage htmlcov build dist *.egg-info

run-normal:
	python -m src.simulation.scenario_runner --scenario configs/scenarios/normal_liquidity.yaml --algo twap