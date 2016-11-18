echo  "
This script will install graphviz,. This assumes a unix system with python 2.7 and pip already installed. 
This script also automatically trains the TDIDT based on train data given in data/ and runs the test module as well.
HINT: Hit Enter to Continue, or ctrl+C to quit this script.


"
read
sudo pip install graphviz
python tdidt_train.py
python tdidt_test.py
