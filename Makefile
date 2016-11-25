clean:
	-rm -rf *.pyc
	-rm -rf *.hlt
	-rm -rf *.log
	-rm -rf *.zip

build:
	zip -r jzebra.zip . -x .\* halite __pycache__/\* Makefile