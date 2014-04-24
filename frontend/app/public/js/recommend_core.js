var globalName = "";
$(window).load(function()
	{
        //for recommended reading - without bfs
        //FIrst set of images for book names , we need to get from http://www.comicvine.com/api/characters?api_key=37a0f6cdbe5752b2f272373ba6a21491ea2629eb&filter=name:superman&format=json
            //get names first from localhost:8080/api/getcomics:globalName
           
            console.log("here");
            var comicname = new Array();
            loadParameters();
            var images = [];
            $.get("http://localhost:8081/api/nodes:"+globalName, function(req,res)
            {
                
                var i=0;
                for (idx in req['nodes'])
                {
                    console.log(req['nodes'][idx]['image']);
                    var a = req['nodes'][idx]['nameid'];
                    a = a.replace(" ","%20");
                    console.log(a);
                    if(req['nodes'][idx]['image'])
                        $('#carousel_ul').append('<li><div class="imagecontainer"><a href=http://localhost:8081/recommend?name='+a+'><table><tr><img src="'+req['nodes'][idx]['image']+'"/></tr><tr><center>'+req['nodes'][idx]['nameid']+'</center></tr></table></a></div></li>') ;
                }
                
            },"json");

            $.get("http://localhost:8081/api/getcomics:"+globalName, function(req,res)
            {
                
                var i=0;
                for (idx in req)
                {
                    $('#carousel_ul1').append('<center><li><a href=http://www.amazon.com/Batman-The-Dark-Knight-Returns/dp/1563893428>'+req[idx]+'</a></li></center>') ;
                    if (idx>6)
                        break;
                }
                if (req.length==0)
                {
                     $.get("http://localhost:8081/api/getcomics:batman", function(req,res)
                     {
                         for (idx in req)
                        {
                            $('#carousel_ul1').append('<center><li><a href=http://www.amazon.com/Batman-The-Dark-Knight-Returns/dp/1563893428>'+req[idx]+'</a></li></center>') ;
                            if (idx>6)
                                break;
                        }
                     }, "json");
                }
                
            },"json");
            
            //then take 5 of those names and slice it to 2 and pass it to the 2nd get call. Final images, append to carousel_ul
			//We need to get the image
             
            $('#carousel_ul li:first').before($('#carousel_ul li:last'));    
            $('#right_scroll img').click(function()
            {
                var item_width = $('#carousel_ul li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul').css('left')) - item_width;

                $('#carousel_ul:not(:animated)').animate({'left' : left_indent},500,function()
                {    
	                    $('#carousel_ul li:last').after($('#carousel_ul li:first')); 
	                    $('#carousel_ul').css({'left' : '-210px'});
                }); 
            });
            $('#left_scroll img').click(function()
            {                    
                var item_width = $('#carousel_ul li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul').css('left')) + item_width;                    
                $('#carousel_ul:not(:animated)').animate({'left' : left_indent},500,function()
                {         
		                $('#carousel_ul li:first').before($('#carousel_ul li:last')); 
		                $('#carousel_ul').css({'left' : '-210px'});
                });   
            });

            $('#carousel_ul_1 li:first').before($('#carousel_ul_1 li:last')); 
            $('#right_scroll_1 img').click(function()
            {
                var item_width = $('#carousel_ul_1 li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul_1').css('left')) - item_width;

                $('#carousel_ul_1:not(:animated)').animate({'left' : left_indent},500,function()
                {    
	                    $('#carousel_ul li_1:last').after($('#carousel_ul_1 li:first')); 
	                    $('#carousel_ul_1').css({'left' : '-210px'});
                }); 
            });
            $('#left_scroll_1 img').click(function()
            {                    
                var item_width = $('#carousel_ul_1 li').outerWidth() + 10;
                var left_indent = parseInt($('#carousel_ul_1').css('left')) + item_width;                    
                $('#carousel_ul_1:not(:animated)').animate({'left' : left_indent},500,function()
                {         
		                $('#carousel_ul_1 li:first').before($('#carousel_ul_1 li:last')); 
		                $('#carousel_ul_1').css({'left' : '-210px'});
                });   
            });


      });

/*
$(window).load(function() {
 // executes when complete page is fully loaded, including frames,objects and images
 loadParameters();
 console.log("SDfsdfsdf"+globalName)
});
*/

function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
}

function httpGet(theUrl)
{
     var url = 'http://www.comicvine.com/api/characters/';
      console.log("url"+url)
     $.ajax({
                url: 'http://www.comicvine.com/api/characters/',
                api_key: '37a0f6cdbe5752b2f272373ba6a21491ea2629eb',
                filter: 'name:superman',
                crossDomain: true,
                format: 'json',
                type: 'GET',
                success: function(){
                    alert("success");
                }
            });
}

function loadParameters()
{
	var name = getURLParameter('name');
	globalName = name;
}

function firstDiv()
{
	alert("Global name is "+globalName);
}
function helloWorld()
{
	alert("hello, world!");
}
