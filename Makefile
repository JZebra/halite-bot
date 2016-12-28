clean:
	-rm -rf *.pyc
	-rm -rf *.hlt
	-rm -rf *.log
	-rm -rf *.zip

build:
	zip -r jzebra.zip . -x .\* halite __pycache__/\* Makefile

restart:
	ps ax | grep -i pipe_socket_translator.py | awk 'NR==1{print $$1}' | xargs kill
	sleep 1
	./runGame.sh