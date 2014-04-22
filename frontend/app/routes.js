
module.exports = function(app,neo4j) 
{
    var db = new neo4j.GraphDatabase('http://localhost:7474');
	// application ==============================================
	app.get('/index', function(req, res) {
		res.sendfile('./app/view/index.html'); 
	});

	app.get('/recommend', function(req, res) {
		res.sendfile('./app/view/recommend.html'); 
	})

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
/*
def get_heroes():
  #return pickle.load(open('heroes_100.pkl'))
  return ["Batman"]

list_of_heroes=get_heroes()

for hero in list_of_heroes:
  url = 'http://dc.wikia.com/wiki/'+hero+'_Recommended_Reading'
  soup = bs(ulib2.urlopen(url).read())
  for header in soup.findAll('h2'):
    print '\n'+header.text
    for item in header.findNextSiblings()[0].findAll('li'):
      print item.a.text
print "done"*/


app.get('/api/getcomics', function(req, res) {

var jsdom  = require('jsdom');
var fs     = require('fs');
var jquery = fs.readFileSync("./jquery.js").toString();

jsdom.env({
  html: 'http://news.ycombinator.com/',
  src: [ jquery ],
  done: function(errors, window) {
    var $ = window.$;
    $('a').each(function(){
      console.log( $(this).attr('href') );
    });
  }
});

/*
      var hero='batman'
      var url = ['http://dc.wikia.com/wiki/'+hero+'_Recommended_Reading'].join('\n');
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
    

});*/

    });
};
