deploy:
	deploy/push
	deploy/install
	@echo "\nRemember to update the config.py file if needed!"

server:
	env FLASK_APP=mpi/web.py FLASK_DEBUG=1 pipenv run flask run

.PHONY: deploy server
