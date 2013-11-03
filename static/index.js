
window.ScatterPlot = function($, d3, nv){

  var sp = {};

  sp.randomData = function (groups, points) { //# groups,# points per group
    var data = [],
        shapes = ['circle', 'cross', 'triangle-up', 'triangle-down', 'diamond', 'square'],
        random = d3.random.normal();
  
    for (i = 0; i < groups; i++) {
      data.push({
        key: 'Group ' + i,
        values: []
      });
  
      for (j = 0; j < points; j++) {
        data[i].values.push({
          x: random()
        , y: random()
        , size: Math.random()
        //, shape: shapes[j % 6]
        });
      }
    }
  
    return data;
  };


  
  sp.getData = function(){
    $.when( 
      $.getJSON("practices/metric/random"), 
      $.getJSON("practices/metric/random")
    ).then(
      function(metrica, metricb){
        var random = d3.random.normal();
        
        console.log(metrica, metricb);
        
        var datum = { 
          key: "General Practices",
          values: []
        };
        
        metrica[0].forEach(function(v){
          datum.values.push({
            size: 1,
            x: v.metrics.random,
            y: random(),
          });
        });
        
        console.log(datum);

        sp.plot("#chart svg", [datum]);
        
      },
      function(){
        alert("Error ocurred when loading data.");
      }
    ); 
  };

  sp.plot = function(target, data){
    nv.addGraph(function() {
      var chart = nv.models.scatterChart()
                    .showDistX(true)
                    .showDistY(true)
                    .color(d3.scale.category10().range());
    
      chart.xAxis.tickFormat(d3.format('.02f'))
      chart.yAxis.tickFormat(d3.format('.02f'))
    
      d3.select(target)
          .datum(data)
        .transition().duration(500)
          .call(chart);
    
      nv.utils.windowResize(chart.update);
    
      return chart;
    });
  };

  return sp;

}(jQuery, d3, nv);


