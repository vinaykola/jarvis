var jarvisHome = angular.module('jarvisHome',[]);


jarvisHome.controller('mainController', function($scope,$http) {
  $scope.name = 'World';

  $http.get('/js/miserables.json')
       .then(function(res){
          $scope.graphData = res.data;        
        });
});


jarvisHome.directive('d3Graph', function() 
{

      //Size of region to render on
      var width = window.screen.availWidth,
          height = window.screen.availHeight;

      //var color = d3.scale.category20();
      var color = d3.scale.ordinal().range(colorbrewer.PuOr[11].slice(1,12));


      //D3 force directed layout
      //Try playing with the charge and link distance
      var force = d3.layout.force()
          .gravity(0.05)
          .charge(-200)
          .linkDistance(120)
          .size([width, height]);

    return {
        restrict: 'E',
        scope: { val: '='},
        link: function(scope,element,attrs) 
        {
            scope.$watch('val', function() {
                    scope.render(scope.val);
                    });

            scope.render = function(val)
            {

                // If we don't pass any data, return out of the element
                if (!val) return;

                var graph = val;
                //      console.log(graph.nodes);


                var svg = d3.select("body").append("svg")
                  .attr("width", width)
                  .attr("height", height);


                  force
                      .nodes(graph.nodes)
                      .links(graph.links)
                      .start();

                //Add the links
                  var link = svg.selectAll(".link")
                      .data(graph.links)
                      .enter().append("line")
                      .attr("class", "link")
                      .style("stroke-width", function(d) { return Math.sqrt(d.value); })
                      .style("stroke","#000030")

                //Add the nodes
                  var node = svg.selectAll(".node")
                      .data(graph.nodes)
                      .enter()
                      .append("g")            
                      .attr("class", "node")
                      .call(force.drag);

                      //Can be used to select a subset of the data
                      //.filter(function(d){return d.coolness >= 25;})


                      node.append("circle")
                      .attr("r", function(d){ return Math.sqrt(d.coolness)*1.5;})
                      .style("fill", function(d) { return color(d.group); });


                      node.append("text")
                      .attr("x", 19)
                      .attr("dy", ".31em")
                      //uncomment for coloured labels
                      //.style("fill", function(d) { return color(d.group); })
                      .style("fill", "#000000")
                      .text(function(d) 
                      {
                        //uncomment the if condition to show labels for characters where coolness > 25
                        if(d.coolness > 25) 
                          return d.name 
                      });
                      
                           

                //Update stuff for animation:
                //   This takes the physics simulation for the force directed graph and
                //   sets the location of the nodes and edges to the new positions
                  force.on("tick", function() 
                  {
                    link.attr("x1", function(d) { return d.source.x; })
                      .attr("y1", function(d) { return d.source.y; })
                      .attr("x2", function(d) { return d.target.x; })
                      .attr("y2", function(d) { return d.target.y; });

                      // node.attr("cx", function(d) { return d.x; })
                      //    .attr("cy", function(d) { return d.y; });

                      node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
                  });
            }
        }
    };
});