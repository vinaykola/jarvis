
module.exports = function(app,neo4j,fs,request,cheerio) 
{
    var db = new neo4j.GraphDatabase('http://localhost:7474');
	// application ==============================================
	app.get('/index', function(req, res) {
		res.sendfile('./app/view/index.html'); 
	});

	app.get('/recommend', function(req, res) {
		res.sendfile('./app/view/recommend.html'); 
	});

    app.get('/api/edges:todo_id',function(req, res) {
      var _id = req.params.todo_id
        var query = [
      'MATCH n-[r]->m',
      'WHERE n.nameid="'+_id.slice(1)+'"',
      'RETURN n,r,m limit 30;'].join('\n');   
      var output=[];
      console.log(query)
      db.query(query, function (err, results) {
        
        
    if(err)
        res.send(err)
    //console.log(results);
    for (var idx in results) {
        
        if (results.hasOwnProperty(idx)) {

        output.push({source:results[idx]['n']['_data']['data']['nameid'],id:results[idx]['r']['_data']['data']['id'],target:results[idx]['m']['_data']['data']['nameid']});
        }}
    console.log(output)  
      res.json(output)
    

});

    });

 app.get('/api/nodes:nameid',function(req, res) {
      var _id = req.params.nameid
        var query = [
      'MATCH n-[r]->m',
      'WHERE n.nameid="'+_id.slice(1)+'" AND n.nameid=r.orig_edge',
      'RETURN n,r,m limit 30;'].join('\n');   
      var output={'nodes':[],'links':[]};
      console.log(query)
      db.query(query, function (err, results) {
        
        
    if(err)
        res.send(err)
    //console.log(results);
    
    var output1=[];
    var output2=[];
    var integ=0;

    for (var idx in results) {
        
        if (results.hasOwnProperty(idx)) {
                      var a = "Male"
                      if(results[idx]['m']['_data']['data']['gender']=='2')
                        a = "Female"
                      else if(results[idx]['m']['_data']['data']['gender']=='0')
                        a = "Neutral"
            if (integ==0)
            {
              output.nodes.push({name:results[idx]['n']['_data']['data']['name'],id:results[idx]['n']['_data']['data']['name'].split(":")[1],nameid:results[idx]['n']['_data']['data']['nameid'],
              gender:a,image:results[idx]['n']['_data']['data']['image'],count_of_issue_appearances:results[idx]['n']['_data']['data']['count_of_issue_appearances'],
            publisher:results[idx]['n']['_data']['data']['publisher'],creators:results[idx]['n']['_data']['data']['creators']})
              integ=integ+1;
            }

        output.nodes.push({name:results[idx]['m']['_data']['data']['name'],id:results[idx]['m']['_data']['data']['name'].split(":")[1],nameid:results[idx]['m']['_data']['data']['nameid'],
          gender:a,image:results[idx]['m']['_data']['data']['image'],count_of_issue_appearances:results[idx]['m']['_data']['data']['count_of_issue_appearances'],
          publisher:results[idx]['m']['_data']['data']['publisher'],creators:results[idx]['m']['_data']['data']['creators']})
        output.links.push({source:results[idx]['n']['_data']['data']['name'],id:results[idx]['r']['_data']['data']['id'],target:results[idx]['m']['_data']['data']['name']})
        }}
       
    console.log(output)  
      res.json(output)
    

});

    });


    app.get('/api/allnodes', function(req, res) {

      var query1 = ['MATCH n RETURN n.nameid as names;'].join('\n');
    

      var output=[];
      console.log("asdf")
      db.query(query1, function (err, results) {
    
    console.log(results);    
    if(err)
        res.send(err)

    for (var idx in results) {
        output.push(results[idx].names)
       }

      res.json(output)
      
    

});

    });





app.get('/api/getcomics:character', function(req, res) {

  var charname = req.params.character
  console.log(charname)
  url = 'http://dc.wikia.com/wiki/'+charname.slice(1)+'_Recommended_Reading'
  console.log(url)
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
              try
              {
                    var comic=childs[child].children[0].next.children[0].attribs.title
                    var comic_name = comic.replace(" (page does not exist)","");
                    
                    output.push(comic_name)
              }
              catch(err)
              {
                console.log(err)

              }
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



};
