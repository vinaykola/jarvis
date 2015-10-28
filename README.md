jarvis
======

A visual recommender system for the comic book universe

The project was built on the MVC Framework. The data was obtained from the comicvine api with a variety of features(about 20) being extracted for all characters (about 78000). The model consists of the database files of neo4j, and the api methods were built using javascript and python. The database was populated with the help of batch-import (jexp/batch-import) package available in git, which runs neo4j cypher queries in java. A total of 56000 nodes and 560000 edges were inserted in about 20 seconds. 

The controller was also built on javascript, which dealt with apis for the view. The major apis were node information, edges information for a node, recommended comics for a particular node. 

The view was built on javascript, html and css. There are 2 major html files with their corresponding javascript files - index.html that deals with the main graph visualization, search box and info box for characters, and was built using angularjs and D3. The user is redirected to the recommendation page when he/she clicks recommend from the info box. The recommendation page was built in jquery.

Installation Information

Clone the repository. Install nodemon and angular libraries to run the package. Install neo4j for the database. 

1) Install Nodejs on the machine
	
	sudo apt-get install nodejs

also run,

	sudo apt-get install nodejs-legacy

or download the binary from here : http://nodejs.org/download/ Ensure that the installed version is 0.10.26

2) Once node js is installed, install npm using the command 

	sudo apt-get install npm

 then run the following command in the /frontend folder which has the package.json file in it

	sudo npm install 

3) Now install nodemon using the following command in the same folder -

	sudo npm install -g nodemon


4) Once nodemon is installed the neo4j database needs to be set up. This can be done by first installing neo4j 

	sudo apt-get install neo4j

	We are currently working on version 2.0.2 of the software

Copy and replace the neo4j data folder (/var/lib/neo4j/data) with the one in the repository. Edit the neo4j.properties file (in /etc/neo4j) and uncomment the following lines : 
```
allow_store_upgrade=true
keep_logical_logs=true
node_auto_indexing=true
node_keys_indexable=name
relationship_auto_indexing=true
relationship_keys_indexable=name
```
Go to the main folder of the neo4j database : /var/lib/neo4j and run sudo ./bin/neo4j start on the terminal. This will start the neo4j database server at port 7474. You can view and use the console at http://localhost:7474/webadmin/#/console/ . 

5) Return to the main folder of the project jarvis/frontend and run the following command to start a server on localhost:8081

	nodemon server.js

6) You can now access the website at the following URL http://localhost:8081/index

To use the project:

1. It starts of with the graphical representation of Batman along with 10 characters most similar to him. To celebrate the 75th anniversary of Batman, we have set him as our default character. You can search for any character from the search box on the top left corner of the index page. The seach box auto suggests search options to the user as soon as he starts typing.
2. Single clicking a node displays the information box for that particular character. Clicking 'Recommend' on the bottom of the page, redirects you to the recommendations page for that character, which displays the recommended characters the user can follow based on his selection, as well as a list of recommended readings for that particular character. Clicking the picture of a recommended character in the carousal redirects you to that characters recommendations page. Clicking any one of the recommended readings redirects you to the eBay portal, where you can purchase that particular comic.
3. Double clicking a node expands the graph by showing the 10 most similar characters to that particular character. You can continue double clicking and expanding the graph. This is exactly the point of this project : To enable the user to explore the comic book universe, by merging various other universes together to form a huge comic multiverse and providing a visualization that gives the user an enjoyable experience while exploring the universe.
4. Zooming and panning are additional functionalities offered. As the graph expands, it becomes congested so in order to enable the user to discern the labels in a congested network, the zooming in and the panning features are offered.

Now, you are all set to explore a universe full of superheros and find out how to catch up with your favourite ones, as well as discover some new ones along the way!
