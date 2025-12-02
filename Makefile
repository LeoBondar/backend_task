.PHONY: run

default: run

define set-default-container
	ifndef c
	c = app
	else ifeq (${c},all)
	override c=
	endif
endef

set-container:
	$(eval $(call set-default-container))

build: set-container
	docker compose build ${c}

dev:
	docker compose up -d --force-recreate ${c}

restart: set-container
	docker compose restart ${c}

down:
	docker compose down

exec: set-container
	docker compose exec ${c} /bin/bash

log: set-container
	docker compose logs -f ${c}

local_run:
	HOT_RELOAD=true python3 backend.py

format:  ## Autoformat code
	flake8 . tests
	mypy app
	safety check
	bandit -r app

lint:
	ruff check . tests
	mypy .
	safety check
	bandit -r app
