window.onload = function() {

    var accuracyChart = new CanvasJS.Chart("accChart", {
        theme: "light1", // "light1", "light2", "dark1", "dark2"
        exportEnabled: true,
        animationEnabled: true,
       
        data: [{
            type: "pie",
            startAngle: 25,
            toolTipContent: "<b>{label}</b>: {y}%",
            showInLegend: "true",
            legendText: "{label}",
            indexLabelFontSize: 13,
            indexLabel: "{label}  {y}%",
            dataPoints: [
                { y: 91, label: "accurate" },
                { y: 9, label: "Inaccurate" },
                
            ]
        }]
    });
    accuracyChart.render();


        var mcfccGraph = new CanvasJS.Chart("mcfccChart", {
          theme: "light1", // "light1", "light2", "dark1"
          animationEnabled: true,
          exportEnabled: true,
          
          axisX: {
            margin: 10,
            labelPlacement: "inside",
            tickPlacement: "inside"
          },
          axisY2: {
            
            titleFontSize: 14,
            includeZero: true,
            suffix: ""
          },
          data: [{
            type: "bar",
            axisYType: "secondary",
            yValueFormatString: "#,###.##",
            indexLabel: "{y}",
            dataPoints: [
                //add var from backend insted of each y
              { label: "Esraa", y: 4.25 },
              { label: "Mariam", y: 4.00 },
              { label: "Nasser", y: 3.93 },
              { label: "Abdelrahman", y: 3.72 },
              
            ]
          }]
        });
        mcfccGraph.render();
    
    }