# browsing-history-analyser

This repo contains code that lets the user create profile from their Firefox browsing history. Please note that this is very early code, with a number of issues to be solved. However, we appreciate test reports!!

## Instructions

First, make sure you have a local PeARS install. (In the following, we'll assume you have a ~/PeARS/ directory on your machine, cloned from https://github.com/PeARSearch/PeARS.)

Clone the present repo:

`git clone https://github.com/PeARSearch/browsing-history-analyser.git`

Make sure you have all needed dependencies:

`pip install -r requirements.txt`

Link to the semantic space in your PeARS install:

`ln -s ~/PeARS/openvectors.db .`


To index (some of) your browsing history, run the analyser:

`python run_analyser.py`

To search, copy the necessary files to your local PeARS install. 

`cp -r local-history ~/PeARS/demo/users/`

Then, move to your PeARS install and update your shared_pears_ids.txt file:

`cd ~/PeARS`

`egrep "pear_id" demo/users/local-history/profile.txt |sed "s/pear_id:/demo\/users\/local-history /" >> app/shared_pears_ids.txt`

You're ready to search!

`python run.py`
