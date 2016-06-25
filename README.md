# browsing-history-analyser

A repo for the local browsing history analyser, which lets the user see the topics of what they've browsed.

The requirements are:

* A daemon which checks the http/https calls from the system. It should insert the appropriate urls in a database. 
* The parser (create_history_db.py and retrieve_pages.py, currently in the root of the PeARS repo).
* Some distributional semantics code to produce vectors from documents.
* A clustering algorithm, which clusters vectors by similarity and puts helpful keywords on each cluster.
* A GUI that lets the user pick which clusters they want to share on the network, together with a program that will produce a vector database for the retained documents, and delete the rest.
