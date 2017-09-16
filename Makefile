# Makefile for Sanity

# If target is 'newnote'
ifeq (newnote,$(firstword $(MAKECMDGOALS)))
  # use rest as arguments
  NEW_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # and make them do-nothing targets
  $(eval $(NEW_ARGS):;@:)
endif

all:
	echo "This just saved you from a terrible mistake!"

.PHONY: docs
docs:
	tox -e docs

.PHONY: releasenotes
releasenotes:
	tox -e releasenotes

.PHONY: newnote
newnote:
	tox -e venv -- reno new $(NEW_ARGS)

test:
	tox

clean:
	rm -rf doc/build test*-e

relnotes:
	@echo "Please use 'make  releasenotes' now"
	@sleep 10
	$(MAKE) releasenotes
