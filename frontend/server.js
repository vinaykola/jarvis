// server.js (final)

	// set up ======================================================================
	var express  = require('express');
	var app      = express(); 								// create our app w/ express
	var port  	 = process.env.PORT || 8080; 				// set the port
	var neo4j = require('neo4j');
	var db = new neo4j.GraphDatabase('http://localhost:7474');


	// configuration ===============================================================
	//Connect to Neo4j here

	app.configure(function() {
		app.use(express.static(__dirname + '/app/public')); 	// set the static files location /public/img will be /img for users
		app.use(express.logger('dev')); 						// log every request to the console
		app.use(express.bodyParser()); 							// pull information from html in POST
		app.use(express.methodOverride()); 						// simulate DELETE and PUT
	});

	// routes ======================================================================
	require('./app/routes.js')(app,neo4j);

	// listen (start app with node server.js) ======================================
	app.listen(port);
	console.log(__dirname);
	console.log("App listening on port " + port);