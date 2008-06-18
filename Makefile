
DOCFILES	= README

default : all

all :
	echo "prout"

install :
	python setup.py install
	
develop :
	python setup.py develop

clean :
	-find -name "*.pyc" -exec rm -f {} \;

