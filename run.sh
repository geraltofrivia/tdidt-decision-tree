echo  "
This script will install graphviz, pickle. This assumes a unix system with python 2.7 and pip already installed. 
HINT: Hit Enter to Continue, or ctrl+C to quit this script.
"
read
sudo pip install graphviz
python tdidt_train.py
python tdidt_test.py
