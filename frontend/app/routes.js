
module.exports = function(app,neo4j,fs,request,cheerio) 
{
    var db = new neo4j.GraphDatabase('http://localhost:7474');
	// application ==============================================
	app.get('/index', function(req, res) {
		res.sendfile('./app/view/index.html'); 
	});

    app.get('/api/edges:todo_id',function(req, res) {
      var _id = req.params.todo_id
        var query = [
      'MATCH n-[r]->m',
      'WHERE n.name="'+_id.slice(1)+'"',
      'RETURN n,m limit 30;'].join('\n');   
      var output=[];
      console.log(query)
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



    app.get('/api/allnodes', function(req, res) {

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



app.get('/api/getcomics:character', function(req, res) {

  var charname = req.params.character
  url = 'http://dc.wikia.com/wiki/'+charname.slice(1)+'_Recommended_Reading'
  request(url, function(error, response, html){
    var output=[];
    if(!error){
      var $ = cheerio.load(html);

      var json = { title : "", release : "", rating : ""};

      $('h2').filter(function(){


            var data = $(this);
            $()
            var childs=data.next()['0'].children
            for (var child in childs){
              var comic=childs[child].children[0].next.children[0].attribs.title
              var comic_name = comic.replace(" (page does not exist)","");
              
              output.push(comic_name)
            }


          })

            
    }
        // To write to the system we will use the built in 'fs' library.
        // In this example we will pass 3 parameters to the writeFile function
        // Parameter 1 :  output.json - this is what the created filename will be called
        // Parameter 2 :  JSON.stringify(json, null, 4) - the data to write, here we do an extra step by calling JSON.stringify to make our JSON easier to read
        // Parameter 3 :  callback function - a callback function to let us know the status of our function

        //fs.writeFile('output.json', JSON.stringify(json, null, 4), function(err){

          //console.log('File successfully written! - Check your project directory for the output.json file');

        //})

        // Finally, we'll just send out a message to the browser reminding you that this app does not have a UI.
        //res.send('Check your console!')
        res.json(output)
  })
})



<<<<<<< HEAD
    });
};
=======
};
>>>>>>> e0f4b080951d2b6d62f7184087a7965c0a98e0d5
