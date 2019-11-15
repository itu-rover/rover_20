
function degrees_to_radian(my_degree){

	var radian = ((my_degree * (1.0))/180)*(Math.PI);
	return radian;
}

window.onload = function(){

	var dps_1 = [{x:10,y:10},{x:0,y:0},{x:0,y:0},{x:0,y:0},{x:0,y:0}]; // dataPoints

	var chart_1 = new CanvasJS.Chart("chartContainer_1", {

		theme: "dark2",
		title :{
			text: "Robotic Arm"
		},
		axisX:{
	        interval: 10
	    },
		axisY: {
			gridThickness: 0,
			interval: 10
		},
		data: [{
			type: "line",
			lineThickness: 20,
			lineColor:"white",
			dataPoints: dps_1
		}]
	});

	chart_1.render();

	var joint_2_angle_int = 0;
	var joint_3_angle_int = 0;
	var joint_5_angle_int = 0;

	function robotic_arm_move(){
	     
		joint_2_angle_int -= 0.2;
		//joint_3_angle_int += 0.2;
		//joint_5_angle_int -= 0.2;

		var joint_2_piece_angle = joint_2_angle_int + 90;
		var joint_3_piece_angle = joint_3_angle_int + joint_2_angle_int;
		var joint_3_half_piece_angle = joint_3_angle_int + joint_2_angle_int + (-90);
		var joint_5_piece_angle = joint_5_angle_int + joint_3_angle_int + joint_2_angle_int;

		var joint_2_piece_endp_x = 10 + 100*(Math.cos(degrees_to_radian(joint_2_piece_angle))); // 10 10 robot kolun başlangıç noktası, 100 ilk parçanın uzunluğu
		var joint_2_piece_endp_y = 10 + 100*(Math.sin(degrees_to_radian(joint_2_piece_angle)));

		var joint_3_piece_endp_x = joint_2_piece_endp_x + 100*(Math.cos(degrees_to_radian(joint_3_piece_angle)));
		var joint_3_piece_endp_y = joint_2_piece_endp_y + 100*(Math.sin(degrees_to_radian(joint_3_piece_angle)));

		var joint_3_half_piece_endp_x = joint_3_piece_endp_x + 25*(Math.cos(degrees_to_radian(joint_3_half_piece_angle)));
		var joint_3_half_piece_endp_y = joint_3_piece_endp_y + 25*(Math.sin(degrees_to_radian(joint_3_half_piece_angle)));

		var joint_5_piece_endp_x = joint_3_half_piece_endp_x + 25*(Math.cos(degrees_to_radian(joint_5_piece_angle)));
		var joint_5_piece_endp_y = joint_3_half_piece_endp_y + 25*(Math.sin(degrees_to_radian(joint_5_piece_angle)));

		dps_1[1] = {x: joint_2_piece_endp_x, y: joint_2_piece_endp_y};
		dps_1[2] = {x: joint_3_piece_endp_x, y: joint_3_piece_endp_y};
		dps_1[3] = {x: joint_3_half_piece_endp_x, y: joint_3_half_piece_endp_y};
		dps_1[4] = {x: joint_5_piece_endp_x, y: joint_5_piece_endp_y};
		
		console.log(dps_1[1])

		chart_1.render();
	};

	setInterval(function(){robotic_arm_move()},33);
}	








