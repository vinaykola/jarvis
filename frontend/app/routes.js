
module.exports = function(app,neo4j) 
{
    var db = new neo4j.GraphDatabase('http://localhost:7474');
	// application ==============================================
	app.get('/index', function(req, res) {
		res.sendfile('./app/view/index.html'); 
	});

    app.get('/api/todos', function(req, res) {

        var query = [
      'MATCH n-[r]->m',
      'WHERE n.name="batman"',
      'RETURN n,m limit 30;'].join('\n');   
      var output=[];

      db.query(query, function (err, results) {
        
        
    if(err)
        res.send(err)
    //console.log(results);
    for (var idx in results) {
        
        if (results.hasOwnProperty(idx)) {
        output.push({source:results[idx]['n']['_data']['data']['name'],target:results[idx]['m']['_data']['data']['name']});
        }}
    console.log(output)  
      res.json(output)
    

});

    });



    app.get('/api/we_are_noobs', function(req, res) {

      var query1 = ['START n=node(*) RETURN n;'].join('\n');
    

      var output=[];
      console.log("asdf")
      db.query(query1, function (err, results) {
    
    console.log(results);    
    if(err)
        res.send(err)
    
    for (var idx in results) {
        
        if (results.hasOwnProperty(idx)) {
        output.push(results[idx]['n']['_data']['data']);
        }}

      res.json(output)
    

});

    });


};