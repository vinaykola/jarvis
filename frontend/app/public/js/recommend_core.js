$(document).ready(function() 
	{
        //for recommended reading - without bfs
        //FIrst set of images for book names , we need to get from http://www.comicvine.com/api/characters?api_key=37a0f6cdbe5752b2f272373ba6a21491ea2629eb&filter=name:superman&format=json
            //get names first from localhost:8080/api/getcomics:globalName
            console.log("here");
            var comicname = new Array();

            $.get("http://localhost:8081/api/getcomics:batman", function(req,res)
            {
                console.log("hi");
               // console.log(req);
                var i=0;
                for (var idx in req)
                {
                    //console.log(req[idx]);
                    comicname[i]=req[idx].split(":")[1].trim();
                    i=i+1;
                    if (i>5)
                        break;
                }
                console.log(comicname)
                //$.get("http://www.comicvine.com/api/issues/?api_key=37a0f6cdbe5752b2f272373ba6a21491ea2629eb&filter=name%3A"+comicname[0]+"&format=json", function(req,res)
                console.log("123");

              url = 'http://www.comicvine.com/api/characters/?api_key=37a0f6cdbe5752b2f272373ba6a21491ea2629eb&filter=name:superman&format=json&callback='
           //   console.log(url)

             console.log(httpGet(url));
            
                


            },"json");

            //then take 5 of those names and slice it to 2 and pass it to the 2nd get call. Final images, append to carousel_ul
			//We need to get the image
            $('#carousel_ul').append('<li><div class="imagecontainer"><img src="http://www.coverbrowser.com/image/batman-dark-knight-returns/3-1.jpg" /></div></li>')   
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

var globalName = "";

function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
}

function httpGet(theUrl)
{
     var url = 'http://www.comicvine.com/api/characters/';
      console.log(url)
    return $http.jsonp(url, {
        params: {
            callback: 'JSON_CALLBACK',
            filter: 'name:superman',
            format:'json',
            api_key: '37a0f6cdbe5752b2f272373ba6a21491ea2629eb'
        }
    });
}

function loadParameters()
{
	var name = getURLParameter('name');
	alert("the name parameter is "+name);
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
