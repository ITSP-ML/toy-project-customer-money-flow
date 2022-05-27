#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = toy-project-customer-money-flow

#################################################################################
# COMMANDS                                                                      #
#################################################################################

#update the environment after manually changing environment.yml
environment.lock: environment.yml
	conda env update -n $(PROJECT_NAME) -f $< --prune
	conda env export -n $(PROJECT_NAME) -f $@

#shortcut for environment update
env: environment.lock