deploy:
	deploy/push
	deploy/install
	@echo "\nRemember to update the config.py file if needed!"

server:
	env FLASK_DEBUG=1 pipenv run python3 mpi/web.py

.PHONY: deploy server
