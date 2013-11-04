
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

  sp.buildMenu  = function(selector){
    $.when(
      $.get("template/metric-dropdown.html"),
      $.getJSON("practices/metrics")
    ).then(function(dropdown,metrics){
      var template = Hogan.compile(dropdown[0]);
      var metrics = metrics[0].available_metrics.map(function(metric){
        return {name: metric, metric: metric}
      }); 
      ["X-Axis", "Y-Axis"].forEach(function(control){
          var data = {
            control: control, 
            control_name:control, 
            metrics: metrics
          };
          $("#choices").append(template.render(data));
      });
    });
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
  sp.encodeMetricName = function(name){
    return btoa(name); 
  };
  sp.compare = function(x_metric, y_metric, size_metric, color_metric){
    if( !x_metric || !y_metric){ 
      console.log("We don't mess with the graph until we have two metrics");
      return null;
    };

    $.when( 
      $.getJSON("practices/compare/"+sp.encodeMetricName(x_metric)+"/"+sp.encodeMetricName(y_metric)+"/2000") 
    ).then(
      function(metrics){
        var datum = { 
          key: "General Practices",
          values: []
        };
        metrics.forEach(function(practice){
          datum.values.push({
            size: 1,
            x: parseFloat(practice.metrics[x_metric]),
            y: parseFloat(practice.metrics[y_metric]),
          });
        });
        
        $("#datapoints").html( datum.values.length);
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

  sp.controller = function(elem){
     var controlFor = $(elem).attr("control-for");
     var metric = $(elem).attr("metric");
     sp[controlFor] =  metric;
     $("#xlabel").html(sp["X-Axis"]);
     $("#ylabel").html(sp["Y-Axis"]);
     sp.compare(
        sp["X-Axis"],
        sp["Y-Axis"],
        sp["Size"],
        sp["Color"]
     );
  };
  
  sp["X-Axis"] = "";
  sp["Y-Axis"] = "";
  sp["Color"] = "";
  sp["Size"] = "";

  return sp;

}(jQuery, d3, nv);


