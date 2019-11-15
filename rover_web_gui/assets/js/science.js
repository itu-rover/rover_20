
window.onload = function () {

	var dps_1 = []; // dataPoints
	var dps_2 = []; // dataPoints
	var dps_3 = []; // dataPoints
	var dps_4 = []; // dataPoints
	var dps_5 = []; // dataPoints
	var dps_6 = []; // dataPoints

	var chart_1 = new CanvasJS.Chart("chartContainer_1", {
		title :{
			text: "Dynamic Data"
		},
		axisY: {
			includeZero: false
		},
		data: [{
			type: "line",
			dataPoints: dps_1
		}]
	});

	var chart_2 = new CanvasJS.Chart("chartContainer_2", {
		title :{
			text: "Dynamic Data"
		},
		axisY: {
			includeZero: false
		},
		data: [{
			type: "line",
			dataPoints: dps_2
		}]
	});

	var chart_3 = new CanvasJS.Chart("chartContainer_3", {
		title :{
			text: "Dynamic Data"
		},
		axisY: {
			includeZero: false
		},
		data: [{
			type: "line",
			dataPoints: dps_3
		}]
	});

	var chart_4 = new CanvasJS.Chart("chartContainer_4", {
		title :{
			text: "Dynamic Data"
		},
		axisY: {
			includeZero: false
		},
		data: [{
			type: "line",
			dataPoints: dps_4
		}]
	});

	var chart_5 = new CanvasJS.Chart("chartContainer_5", {
		title :{
			text: "Addable Data"
		},
		axisY: {
			includeZero: false
		},
		data: [{
			type: "line",
			dataPoints: dps_5
		}]
	});

	var chart_6 = new CanvasJS.Chart("chartContainer_6", {
		title :{
			text: "Addable Data 2"
		},
		axisY: {
			includeZero: false
		},
		data: [{
			type: "line",
			dataPoints: dps_6
		}]
	});

	chart_5.render();
	chart_6.render();

	function addDataPointsAndRender() {
			xValue = Number(document.getElementById("xValue").value);
			yValue = Number(document.getElementById("yValue").value);
			dps_5.push({
					x: xValue,
					y: yValue
			});
			chart_5.render();
	}

	function addDataPointsAndRender2() {
			xValue = dps_6.length + 1;
			yValue = Number(document.getElementById("yValue2").value);
			dps_6.push({
					x: xValue,
					y: yValue
			});
			chart_6.render();
	}

	function deleteLastDataAndRender() {
			dps_5.pop();
			chart_5.render();
	}

	function deleteLastDataAndRender2() {
			dps_6.pop();
			chart_6.render();
	}

	var renderButton1 = document.getElementById("renderButton1");
	var renderButton2 = document.getElementById("renderButton2");

	var deleteButton1 = document.getElementById("deleteButton1");
	var deleteButton2 = document.getElementById("deleteButton2");

	renderButton1.addEventListener("click", addDataPointsAndRender);
	renderButton2.addEventListener("click", addDataPointsAndRender2);

	deleteButton1.addEventListener("click", deleteLastDataAndRender);
	deleteButton2.addEventListener("click", deleteLastDataAndRender2);

	var xVal_1 = 0;
	var xVal_2 = 0;
	var xVal_3 = 0;
	var xVal_4 = 0;
	var yVal_1 = 100;
	var yVal_2 = 100;
	var yVal_3 = 100;
	var yVal_4 = 100;

	var updateInterval = 1000;
	var dataLength = 20; // number of dataPoints visible at any point

	var updateChart_1 = function (count) {

		count = count || 1;

		for (var j = 0; j < count; j++) {
			yVal_1 = yVal_1 +  Math.round(5 + Math.random() *(-5-5));
			dps_1.push({
				x: xVal_1,
				y: yVal_1
			});
			xVal_1++;
		}

		if (dps_1.length > dataLength) {
			dps_1.shift();
		}

		chart_1.render();
	};

	var updateChart_2 = function (count) {

		count = count || 1;

		for (var j = 0; j < count; j++) {
			yVal_2 = yVal_2 +  Math.round(5 + Math.random() *(-5-5));
			dps_2.push({
				x: xVal_2,
				y: yVal_2
			});
			xVal_2++;
		}

		if (dps_2.length > dataLength) {
			dps_2.shift();
		}

		chart_2.render();
	};

	var updateChart_3 = function (count) {

		count = count || 1;

		for (var j = 0; j < count; j++) {
			yVal_3 = yVal_3 +  Math.round(5 + Math.random() *(-5-5));
			dps_3.push({
				x: xVal_3,
				y: yVal_3
			});
			xVal_3++;
		}

		if (dps_3.length > dataLength) {
			dps_3.shift();
		}

		chart_3.render();
	};

	var updateChart_4 = function (count) {

		count = count || 1;

		for (var j = 0; j < count; j++) {
			yVal_4 = yVal_4 +  Math.round(5 + Math.random() *(-5-5));
			dps_4.push({
				x: xVal_4,
				y: yVal_4
			});
			xVal_4++;
		}

		if (dps_4.length > dataLength) {
			dps_4.shift();
		}

		chart_4.render();
	};

	updateChart_1(dataLength);
	updateChart_2(dataLength);
	updateChart_3(dataLength);
	updateChart_4(dataLength);
	setInterval(function(){updateChart_1()}, updateInterval);
	setInterval(function(){updateChart_2()}, updateInterval);
	setInterval(function(){updateChart_3()}, updateInterval);
	setInterval(function(){updateChart_4()}, updateInterval);

	document.getElementById("exportChart_1").addEventListener("click",function(){
    	chart_1.exportChart({format: "jpeg"});
    });

    document.getElementById("exportChart_2").addEventListener("click",function(){
    	chart_2.exportChart({format: "jpeg"});
    });

    document.getElementById("exportChart_3").addEventListener("click",function(){
    	chart_3.exportChart({format: "jpeg"});
    });

    document.getElementById("exportChart_4").addEventListener("click",function(){
    	chart_4.exportChart({format: "jpeg"});
    });

    document.getElementById("exportChart_5").addEventListener("click",function(){
    	chart_5.exportChart({format: "jpeg"});
    });

    document.getElementById("exportChart_6").addEventListener("click",function(){
    	chart_6.exportChart({format: "jpeg"});
    });

}
