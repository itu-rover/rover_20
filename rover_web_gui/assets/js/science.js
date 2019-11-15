mapboxgl.accessToken = 'pk.eyJ1IjoiZGVrc3ByaW1lIiwiYSI6ImNqOGsxb3dyYzA4b2wyeHBsdGx0aXdzeHYifQ.4vYgxeGhICEGWbC1552LsQ';

var ros_server_url = document.location.hostname + ":9090";
var ros = new ROSLIB.Ros();
var rosConnected = false;



var bio_data;

var ec_data;

var ph_data;
var down = "";
var doubledown = "";
var up = "";
var doubleup = "";

var sledge;
var x;
var a;
var science = new String;
var science_array = ["s", 0, 0, 0, 0, 0, "f"];
var science_publisher;


var data_bio = [60, 45];
var data_ec = [80, 46];
var data_ph = [40, 90];


var dps_bio = [];
var dps_ec = [];
var dps_ph = [];





window.gamepad = new Gamepad();
var focused = false;
var monument = [-110.791941, 38.406320];
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/satellite-streets-v9',
    center: [-110.791941, 38.406320],
    zoom: 18
});
map.addControl(new mapboxgl.NavigationControl(), 'bottom-right');
map.doubleClickZoom.disable();

ros.on("connection", function () {
    console.debug("Connected to ROS server");
    rosConnected = true;
    initPublishers();
    initSubscribers();
    chart.render();
});

ros.on("close", function () {
    console.debug("Disconnected from ROS server");
    rosConnected = false;
});

// Create connection
ros.connect("ws://" + ros_server_url);

var publisher = new ROSLIB.Topic({
    ros: ros,
    name: '/sci',
    messageType: 'std_msgs/String'
});


//science_publisher.publish(science);

function initSubscribers() {

    ////Define subscribers

    var bio_listener = new ROSLIB.Topic({
        ros: ros,
        name: 'bio_data', //dinlenecek topic adı
        messageType: 'std_msgs/Int32MultiArray' //topicin mesaj tipi
    });

    var ec_listener = new ROSLIB.Topic({
        ros: ros,
        name: 'ec_data',
        messageType: 'std_msgs/Int32MultiArray'
    });

    var ph_listener = new ROSLIB.Topic({
        ros: ros,
        name: 'ph_data',
        messageType: 'std_msgs/Int32MultiArray'
    });




    bio_listener.subscribe(function (msg) {
        data_bio = msg.data;
    });
    dust_ec.subscribe(function (msg) {
        data_ec = msg.data;
    });

    ph_listener.subscribe(function (msg) {
        data_ph = msg.data;
    });

}

 initPublishers();
    initSubscribers();


window.onload = function () {

    var chart = new CanvasJS.Chart("chartContainer", {


        backgroundColor: "#d2d6de ",
        animationEnabled: true,
        title: {
            text: "BIOSENSOR-EC-PH"
        },
        exportEnabled: true,
        axisX: {
            title: "Value"

        },
        axisY: {
            title: "Time"
        },
        data: [{
                type: "scatter",
                toolTipContent: "<span style=\"color:#4F81BC \"><b>{name}</b></span><br/><b> Value:</b> {x} <br/><b> Time:</b></span> {y} s",
                name: "BIO",
                showInLegend: true,
                dataPoints: [
                    {
                        x: data_bio[0],
                        y: new Date().getMinutes()
                    },

		]

	},
            {
                type: "scatter",
                toolTipContent: "<span style=\"color:#4F81BC \"><b>{name}</b></span><br/><b> Value:</b> {x} <br/><b> Time:</b></span> {y} s",
                name: "PH",
                showInLegend: true,
                dataPoints: [
                    {
                        x: data_ph[0],
                        y: new Date().getMinutes()
                    },

		]
	},
            {
                type: "scatter",
                name: "EC",
                showInLegend: true,
                toolTipContent: "<span style=\"color:#4F81BC \"><b>{name}</b></span><br/><b> Value:</b> {x} <br/><b> Time:</b></span> {y} s",
                dataPoints: [
                    {
                        x: data_ec[0],
                        y: new Date().getMinutes()
                    },

		]
	}]
    });

    chart.render();
    document.getElementById("exportChart").addEventListener("click", function () {
        chart.exportChart({
            format: "jpg"
        });
    });

}


function myFunction() {

  var x = document.getElementById("myInput").value;
    var y = 2;
    var z;
   
    if (parseFloat(x)>80){
       y = 4;
        z = "up";
   } 
     else if (  parseFloat(x)>60){
      y = 3;
         z = "slowly up";
   } else if ( parseFloat(x)>40) {
       y = 2;
        z = "stop";
   }else if ( parseFloat(x)>20) {
       y = 1;
        z = "slowly down";
   }else if ( parseFloat(x)>0) {
       y = 0;
        z = "down";
   }else {
       y = 2;
       z = "stop";
   }
     science_array[4] = y;
    initPublishers();
  
   
    console.log (y);
    console.log(science_str);
   
  document.getElementById("demo").innerHTML = "You wrote: " + z;


}



console.log(science_array);

science_str = science_array.toString();



var science = new ROSLIB.Message({data : science_str });

function initPublishers() {
    setInterval(function (e) {
        publisher.publish(science);
        console.log(science);
    },3000);
}

console.log(science);



