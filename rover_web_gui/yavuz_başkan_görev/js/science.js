
function string_to_angle(my_string){

	var sign = '+';

	if(my_string.charAt(0) == '1'){

		sign = '-';
	}	

	var int_form = parseInt(my_string) % 1000;

	if(sign == '-'){

		return int_form * (-1);
	}	
	else{

		return int_form;
	}	
}

function degrees_to_radian(my_degree){

	var radian = ((my_degree * (1.0))/180)*(Math.PI);
	return radian;
}

var rbServer = new ROSLIB.Ros({
	url : 'ws://localhost:9090'
});

rbServer.on('connection', function() {
	var fbDiv = document.getElementById('feedback');
	fbDiv.innerHTML += "<p>Connected to websocket server.</p>";
});

rbServer.on('error', function(error) {
	var fbDiv = document.getElementById('feedback');
	fbDiv.innerHTML += "<p>Error connecting to websocket server.</p>";
});

rbServer.on('close', function() {
	var fbDiv = document.getElementById('feedback');
    fbDiv.innerHTML += "<p>Connection to websocket server closed.</p>";
});

var arm19uiSubsTopic = new ROSLIB.Topic({
    ros : rbServer,
    name : '/arm_19_ui',
    messageType : 'std_msgs/String'
});

var message;
var dps_1 = []; // dataPoints

arm19uiSubsTopic.subscribe(function (msg) {
       
    if(msg){

    	message = msg.data;
    	//console.log(message);
    }

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

    var joint_2_angle_str = message.charAt(5) + message.charAt(6) + message.charAt(7) + message.charAt(8);
	var joint_3_angle_str = message.charAt(10) + message.charAt(11) + message.charAt(12) + message.charAt(13);
	var joint_5_angle_str = message.charAt(20) + message.charAt(21) + message.charAt(22) + message.charAt(23);

	var joint_2_angle_int = string_to_angle(joint_2_angle_str);
	var joint_3_angle_int = string_to_angle(joint_3_angle_str);
	var joint_5_angle_int = string_to_angle(joint_5_angle_str);

	var joint_2_piece_angle = joint_2_angle_int + 90;
	var joint_3_piece_angle = joint_3_angle_int + joint_2_angle_int;
	var joint_3_half_piece_angle = joint_3_angle_int + joint_2_angle_int + (-90);
	var joint_5_piece_angle = joint_5_angle_int + joint_3_angle_int + joint_2_angle_int;

	var joint_2_piece_endp_x = 10 + 100*(Math.cos(degrees_to_radian(joint_2_piece_angle))); // 10 10 robot kolun başlangıç noktası, 100 ilk parçanın uzunluğu
	var joint_2_piece_endp_y = 10 + 100*(Math.sin(degrees_to_radian(joint_2_piece_angle)));

	var joint_3_piece_endp_x = joint_2_piece_endp_x + 100*(Math.cos(degrees_to_radian(joint_3_piece_angle)));
	var joint_3_piece_endp_y = joint_2_piece_endp_y + 100*(Math.sin(degrees_to_radian(joint_3_piece_angle)));

	var joint_3_half_piece_angle_endp_x = joint_3_piece_endp_x + 25*(Math.cos(degrees_to_radian(joint_3_half_piece_angle)));
	var joint_3_half_piece_angle_endp_y = joint_3_piece_endp_y + 25*(Math.sin(degrees_to_radian(joint_3_half_piece_angle)));

	var joint_5_piece_endp_x = joint_3_half_piece_angle_endp_x + 25*(Math.cos(degrees_to_radian(joint_5_piece_angle)));
	var joint_5_piece_endp_y = joint_3_half_piece_angle_endp_y + 25*(Math.sin(degrees_to_radian(joint_5_piece_angle)));

	dps_1.push(
	{
		x: 10,
		y: 10
	},
	{
		x: joint_2_piece_endp_x,
		y: joint_2_piece_endp_y
	},
	{
		x: joint_3_piece_endp_x,
		y: joint_3_piece_endp_y
	},
	{
		x: joint_3_half_piece_angle_endp_x,
		y: joint_3_half_piece_angle_endp_y
	},
	{
		x: joint_5_piece_endp_x,
		y: joint_5_piece_endp_y
	});

	chart_1.render();

	dps_1 = [];
});








