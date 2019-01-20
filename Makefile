deploy:
	deploy/push
	deploy/install
	@echo "\nRemember to update the config.py file if needed!"

.PHONY: deploy
