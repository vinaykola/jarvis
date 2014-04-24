var jarvisHome = angular.module('jarvisHome',['ui.bootstrap']);


jarvisHome.controller('mainController', function($scope,$http) {


      $http.get('/api/nodes:Batman')//'/api/edges:' + $scope.selected)
       .then(function(res){
          $scope.graphData = res.data;
          console.log($scope.graphData);

            $http.get('/api/allnodes')
       .then(function(res){     
          $scope.nodes = res.data;
          console.log($scope.nodes);
          console.log("noobs");
        });
        });


  $scope.searchChar = function() 
  {
    console.log($scope.selected);
    $http.get('/api/nodes:' + $scope.selected)
       .then(function(res){
          $scope.graphData = res.data;
          console.log($scope.graphData);
        });
  }
});

jarvisHome.factory('ComicService',function($http)
{
  return {
    getData : function(nodeid)
    {
      return $http.get('/api/nodeid:' + nodeid)
                   .then(function(res)
                   {
                      console.log("New Data");
                      return res.data;
                    });
    }
  };

});




jarvisHome.directive('d3Graph', function(ComicService) 
{

      //Size of region to render on
      var WIDTH = window.screen.availWidth,
          HEIGHT = window.screen.availHeight,
          SHOW_THRESHOLD = 2.5;

      //var color = d3.scale.category20();
      var color = d3.scale.ordinal().range(colorbrewer.PuOr[11].slice(1,12));

        // Variables keeping graph state
        var activeMovie = undefined;
        var currentOffset = { x : 0, y : 0 };
        var currentZoom = 1.0;

        // The D3.js scales
        var xScale = d3.scale.linear()
          .domain([0, WIDTH])
          .range([0, WIDTH]);

        var yScale = d3.scale.linear()
          .domain([0, HEIGHT])
          .range([0, HEIGHT]);

        var zoomScale = d3.scale.linear()
          .domain([1,6])
          .range([1,6])
          .clamp(true);


      //D3 force directed layout
      //Try playing with the charge and link distance
      var force = d3.layout.force()
          //.gravity(0.25)
          .charge(-500)
          .linkDistance(100)
          .size([WIDTH, HEIGHT]);

    return {
        restrict: 'E',
        scope: { val: '='},
        link: function(scope,element,attrs) 
        {
            //Watch if the data in val has changed
            scope.$watch('val', function(newValue,oldValue) 
            {
              console.log("UI");
              console.log("old");
              console.log(oldValue);
              console.log("new");
              console.log(newValue);
              if(newValue)
                scope.render(newValue);
            });


            //Render UI on screen
            scope.render = function(val)
            {

              if(!val) return;

              var data = val;

              if($("#graph").length > 0)
               $("#graph").remove();

              //Append SVG to the body
              var svg = d3.select("#comicNetwork").append("svg")
                        .attr("width", WIDTH)
                        .attr("height", HEIGHT)
                        .attr("id","graph")
                        .attr("viewBox", "0 0 " + WIDTH + " " + HEIGHT )
                        .attr("preserveAspectRatio", "xMidYMid meet")
                        .call( d3.behavior.zoom() 
                              .x(xScale)
                              .y(yScale)
                              .scaleExtent([1, 6])
                              .on("zoom", doZoom)
                              )
                        .on("dblclick.zoom", null)
                        .append("svg:g")
                        .attr("width", WIDTH)
                        .attr("height", HEIGHT).attr("class","parent");


              var node = svg.selectAll(".node"),
                  link = svg.selectAll(".link"),
                  label = svg.selectAll(".label");

              //svg.selectAll("*").remove();

              function findIndexByKeyValue(obj, key, value)
              {
                  for (var i = 0; i < obj.length; i++) {
                      if (obj[i][key] == value) {
                          return i;
                      }
                  }
                  return -1;
              }

              function findObjectByKeyValue(obj, key, value)
              {
                  for (var i = 0; i < obj.length; i++) {
                      if (obj[i][key] == value) {
                          return obj;
                      }
                  }
                  return null;
              }


              // Movie panel: the div into which the movie details info will be written
              comicInfoDiv = d3.select("#comicInfo");

              var links = data.links;
              var nodes = data.nodes;
              var nodeArray = [];
              var linkArray = [];
              var currentLinks = [];

              // Add the node & link arrays to the layout, and start it
              force
                .nodes(nodeArray)
                .links(linkArray)
                .on("tick", tick);

               /* Add drag & zoom behaviours */
              svg.call( d3.behavior.drag()
                  .on("drag",dragmove) );


            addNodes(nodes,links);


            function getNewNodes(node)
            {
              var local = undefined;
                console.log(node.nameid);
                ComicService.getData(node.name).then(function(response)
                { 
                  local = response;
                  addNodes(local.nodes,local.links);
                });
            }


            function addNodes(nodes,links)
            {
              var i=0,j=0;
              console.log(nodeArray.length);
              console.log(i);
              nodes.forEach(function(nodeData)
              {
                if(findIndexByKeyValue(nodeArray,"name",nodeData.name) == -1)
                {
                  nodeArray.push(nodeData);
                  i++;
                }
              });

              console.log(nodeArray.length);
              console.log(i);

              console.log(nodeArray);
              console.log(links);
              console.log(currentLinks);

              for(i=0;i<links.length;i++)
              {
                console.log("Index");
                console.log(currentLinks.indexOf(links[i].id));
                if(currentLinks.indexOf(links[i].id) == -1)
                {
                  var temp = {};
                  temp.source = nodeArray[findIndexByKeyValue(nodeArray,"name",links[i].source)];
                  temp.target = nodeArray[findIndexByKeyValue(nodeArray,"name",links[i].target)];
                  temp.id = links[i].id;
                  console.log(temp);
                  linkArray.push(temp);
                  currentLinks.push(temp.id);
                  j++;
                }
              }
              console.log("Here");
              console.log(linkArray);
              console.log(nodeArray);

              if(i >0 || j > 0)
                console.log("Start");
                console.log(i);
                console.log(j);
                start();
            }

            function start() 
            {
              console.log("1");
              link = link.data(linkArray, function(d) { return d.source.name + '-' + d.target.name; });
              link.enter().insert("line", ".node").attr("class", "link");
              link.exit().remove();
              
              console.log("2");
              node = node.data(nodeArray, function(d) { return d.name; });
              node.enter().append("circle").attr("r", 10)
              .attr('pointer-events', 'all')
              .attr("class",function(d) { return "node " + d.name; })
              .on("dblclick",getNewNodes)
              .on("click", function(d) { showComicPanel(d); } );

              node.append("title")
              .attr("x", 19)
              .attr("dy", ".31em")
              .text(function(d) 
              {
                  return d.nameid;
              });


              node.exit().remove();
              console.log("3");

              label = label.data(force.nodes(), function(d) { return d.name; });
              label.enter().append('svg:text')
              .attr('x','-3em')
              .attr('y','-1em')
              .attr('pointer-events', 'none') // they go to the circle beneath
              //.attr('id', function(d) { return "lf" + d.index; } )
              .attr('class','label')
              .text( function(d) { return d.nameid; } );

              console.log("4"); 
              force.start();             
            }


              function tick() 
              {
                  repositionGraph(undefined,undefined,'tick');
              }

              /* --------------------------------------------------------------------- */
              /* Move all graph elements to its new positions. Triggered:
                 - on node repositioning (as result of a force-directed iteration)
                 - on translations (user is panning)
                 - on zoom changes (user is zooming)
                 - on explicit node highlight (user clicks in a movie panel link)
                 Set also the values keeping track of current offset & zoom values
              */
              function repositionGraph( off, z, mode ) 
              {
                //console.log( "REPOS: off="+off, "zoom="+z, "mode="+mode );
                console.log(5); 
                // do we want to do a transition?
                var doTr = (mode == 'move');

                // drag: translate to new offset
                if( off !== undefined && (off.x != currentOffset.x || off.y != currentOffset.y ) && mode != "ZOOM" ) 
                {
                  console.log("In parent");
                  g = d3.select('.parent');
                  if( doTr )
                    g = g.transition().duration(500);
                  g.attr("transform", function(d) { return "translate("+off.x+","+off.y+")" } );
                  currentOffset.x = off.x;
                  currentOffset.y = off.y;
                }

                // zoom: get new value of zoom
                if( z === undefined ) 
                {
                   if( mode != 'tick' )
                      return; // no zoom, no tick, we don't need to go further
                    z = currentZoom;
                }
                else
                  currentZoom = z;

                    // move edges
                e = doTr ? link.transition().duration(500) : link;

              
                e.attr("x1", function(d) { return z*(d.source.x); })
                .attr("y1", function(d) { return z*(d.source.y); })
                .attr("x2", function(d) { return z*(d.target.x); })
                .attr("y2", function(d) { return z*(d.target.y); });
            

                // move nodes
                n = doTr ? node.transition().duration(500) : node;

                n.attr("transform", function(d) { return "translate("+z*d.x+","+z*d.y+")" } );

                // move labels
                l = doTr ? label.transition().duration(500) : label;

                l.attr("transform", function(d) { return "translate("+z*d.x+","+z*d.y+")" } );
              }
                    

              /* --------------------------------------------------------------------- */
              /* Perform drag
               */
              function dragmove(d) 
              {
                console.log("DRAG",d3.event);
                offset = { x : currentOffset.x + d3.event.dx,
                y : currentOffset.y + d3.event.dy };
                console.log(currentOffset);
                console.log(offset);
                repositionGraph( offset, undefined, 'drag' );
              }

             /* --------------------------------------------------------------------- */
             /* Perform zoom. We do "semantic zoom", not geometric zoom
             * (i.e. nodes do not change size, but get spread out or stretched
             * together as zoom changes)
             */
             function doZoom( increment ) 
             {
                newZoom = increment === undefined ? d3.event.scale : zoomScale(currentZoom+increment);
                //console.log("ZOOM",currentZoom,"->",newZoom,increment);
                if( currentZoom == newZoom )
                  return; // no zoom change

                // See if we cross the 'show' threshold in either direction
                if( currentZoom<SHOW_THRESHOLD && newZoom>=SHOW_THRESHOLD )
                  svg.selectAll(".label").classed('on',true);

                else if( currentZoom>=SHOW_THRESHOLD && newZoom<SHOW_THRESHOLD )
                  svg.selectAll(".label").classed('on',false);

                // See what is the current graph window size
                s = getViewportSize();
                width  = s.w<WIDTH  ? s.w : WIDTH;
                height = s.h<HEIGHT ? s.h : HEIGHT;

                // Compute the new offset, so that the graph center does not move
                zoomRatio = newZoom/currentZoom;
                newOffset = { x : currentOffset.x*zoomRatio + width/2*(1-zoomRatio),y : currentOffset.y*zoomRatio + height/2*(1-zoomRatio) };
                console.log("offset",currentOffset,"->",newOffset);

                // Reposition the graph
                repositionGraph( newOffset, newZoom, "zoom" );
             }  

              /* ----------------------------------------------------------------------------------*/

              // Get the current size & offset of the browser's viewport window
              function getViewportSize( w ) {
                var w = w || window;
                if( w.innerWidth != null ) 
                  return { w: w.innerWidth, 
                     h: w.innerHeight,
                     x : w.pageXOffset,
                     y : w.pageYOffset };
                var d = w.document;
                if( document.compatMode == "CSS1Compat" )
                  return { w: d.documentElement.clientWidth,
                     h: d.documentElement.clientHeight,
                     x: d.documentElement.scrollLeft,
                     y: d.documentElement.scrollTop };
                else
                  return { w: d.body.clientWidth, 
                     h: d.body.clientHeight,
                     x: d.body.scrollLeft,
                     y: d.body.scrollTop};
              }

               /* Change status of a panel from visible to hidden or viceversa
                   id: identifier of the div to change
                   status: 'on' or 'off'. If not specified, the panel will toggle status
                */
                toggleDiv = function( id, status ) 
                {
                  console.log("In toggle" + id + status);
                  d = d3.select('div#'+id);
                  if( status === undefined )
                    status = d.attr('class') == 'panel_on' ? 'off' : 'on';
                  d.attr( 'class', 'panel_' + status );
                  return false;
                }

                /* --------------------------------------------------------------------- */
                /* Show the details panel for a movie AND highlight its node in 
                   the graph. Also called from outside the d3.json context.
                   Parameters:
                   - new_idx: index of the movie to show
                   - doMoveTo: boolean to indicate if the graph should be centered
                     on the movie
                */
                selectCharacter = function( new_name, doMoveTo ) {

                  // do we want to center the graph on the node?
                  doMoveTo = doMoveTo || false;
                  if( doMoveTo ) 
                  {
                      s = getViewportSize();
                      var tempObj = nodeArray[findIndexByKeyValue(nodeArray,"name",new_name)];
                      width  = s.w<WIDTH ? s.w : WIDTH;
                      height = s.h<HEIGHT ? s.h : HEIGHT;
                      offset = { x : s.x + width/2  - tempObj.x*currentZoom,
                           y : s.y + height/2 - tempObj.y*currentZoom };
                      repositionGraph( offset, undefined, 'move' );
                  }
                  // Now highlight the graph node and show its movie panel
                  //showComicPanel(tempObj);
                }

              /* --------------------------------------------------------------------- */
              /* Show the comic details panel for a given node
               */
              function showComicPanel( node ) {
                // Fill it and display the panel
                comicInfoDiv
                .html( getComicInfo(node,nodeArray) )
                .attr("class","panel_on");
              }

               /* Compose the content for the panel with movie details.
                   Parameters: the node data, and the array containing all nodes
                */
                function getComicInfo( n, nodeArray ) {
                  info = '<div id="cover">';
                  info += '<div class=t style="float: right">' + n.nameid + '</div>';
                  if( n.image )
                    info += '<br><br><img align="left" class="cover" height="250" width="220" src="'+ n.image + '" title="' + n.name + '"/>';
                  info +=
                  '<img src="/img/close.png" class="action" height="25" width="25" style="top: 0px;" title="close panel" onClick="toggleDiv(\'comicInfo\');"/>';

                  info += '<br/></div><div style="clear: both;">'
                  if( n.creators )
                    info += '<div class=f><span class=l>Creators</span>: <span class=g>' 
                         + n.creators + '</span></div>';
                  if( n.publisher )
                    info += '<div class=f><span class=l>Publisher by</span>: <span class=d>' 
                         + n.publisher + '</span></div>';
                  if( n.count_of_issue_appearances )
                    info += '<div class=f><span class=l>Issues Appeared In </span>: <span class=c>' 
                         + n.count_of_issue_appearances + '</span></div>';
                  if( n.gender )
                    info += '<div class=f><span class=l>gender</span>: ' + n.gender + '</div>';
                  if( true )
                    info += '<div class=f><span class=l>powers</span>: ' + n.powers + '</div>';
                  info += '<input background=#000 type=submit value=Recommend  class=clouds-flat-button><span class=l></input></div>';
                  return info;
                }
            } //Scope.render
        } //link
    };//return
});//Directive