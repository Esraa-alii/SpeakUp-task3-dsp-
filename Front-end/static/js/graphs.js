window.onload = function() {

    var chart = new CanvasJS.Chart("chartContainer", {
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
    chart.render();
    
    }