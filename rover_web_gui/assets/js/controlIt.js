mapboxgl.accessToken = 'pk.eyJ1IjoiZGVrc3ByaW1lIiwiYSI6ImNqOGsxb3dyYzA4b2wyeHBsdGx0aXdzeHYifQ.4vYgxeGhICEGWbC1552LsQ';

var ros_server_url = document.location.hostname + ":9090";
var ros = new ROSLIB.Ros();
var focused = false;
var rosConnected = false;
var direction;
var joy_msg1 = new ROSLIB.Message({
    linear: {
        x: 0.0,
        y: 0.0,
        z: 0.0
    },
    angular: {
        x: 0.0,
        y: 0.0,
        z: 0.0
    }
});
var joy_msg2 = new ROSLIB.Message({
    linear: {
        x: 0.0,
        y: 0.0,
        z: 0.0
    },
    angular: {
        x: 0.0,
        y: 0.0,
        z: 0.0
    }
});

var joystickL = nipplejs.create({
            zone: document.getElementById('joy-left'),
            mode: 'static',
            position: { left: '20%', top: '50%' },
            color: 'black',
            size: 100
        });

var joystickR = nipplejs.create({
            zone: document.getElementById('joy-right'),
            mode: 'static',
            position: { left: '80%', top: '50%' },
            color: 'black',
            size: 100
        });

var gps_control_listener = new ROSLIB.Topic({
     ros: ros,
     name: 'gps/control',
     messageType: 'sensor_msgs/NavSatFix'
 });

 function setDronePos() {
     map.getSource('drone').setData(drone);


     if (focused === true && rosConnected) {
         map.setCenter(drone.coordinates);
     }
 }
var joystick_datas1 = new Array();

var joystick_datas2 = new Array();

var joystick_publisher1;

var joystick_publisher2;



var monument = [-110.791941, 38.406320];
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/satellite-streets-v9',
    center: [-110.791941, 38.406320],
    zoom: 18
});
map.addControl(new mapboxgl.NavigationControl(), 'bottom-right');
map.doubleClickZoom.disable();
map.setCenter();
map.dragPan.disable();
ros.on("connection", function () {
    console.debug("Connected to ROS server");
    rosConnected = true;
    initSubscribers();
    initPublishers();
    setInterval(publishJoystics, 500);
});

ros.on("close", function () {
    console.debug("Disconnected from ROS server");
    rosConnected = false;
});

// Create connection
ros.connect("ws://" + ros_server_url);

function initPublishers() {
    joystick_publisher1 = new ROSLIB.Topic({
        ros: ros,
        name: 'rover_joy/cmd_vel',
        messageType: 'geometry_msgs/Twist'
    });

    joystick_publisher2 = new ROSLIB.Topic({
        ros: ros,
        name: 'robotic_arm/data',
        messageType: 'geometry_msgs/Twist'
    });

    joystick_publisher1.publish(joy_msg1);
    joystick_publisher2.publish(joy_msg2);

}


function initSubscribers() {
        
    
    
    gps_control_listener.subscribe(function (msg) {
         console.log(msg.data);
         drone.coordinates[1] = msg.latitude;
         drone.coordinates[0] = msg.longitude;
     });
}

var drone = {
    "type": "Point",
    "coordinates": monument
};


// GeoJSON object to hold our measurement features
var geojson = {
    "type": "FeatureCollection",
    "features": []
};

//heading value fo drone marker


// Used to draw a line between points
//Added comments for Taha
var linestring = {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": []
    }
};



map.on('load', function () {
    // add the GeoJSON above to a new vector tile source
    if (rosConnected) {
        map.addSource('drone', {
            type: 'geojson',
            data: drone
        });

        map.setCenter(drone.coordinates);

        map.addLayer({
            "id": "drone-glow-strong",
            "type": "circle",
            "source": "drone",
            "paint": {
                "circle-radius": 18,
                "circle-color": "#fff",
                "circle-opacity": 0.4
            }
        });

        map.addLayer({
            "id": "drone-glow",
            "type": "circle",
            "source": "drone",
            "paint": {
                "circle-radius": 40,
                "circle-color": "#fff",
                "circle-opacity": 0.1
            }
        });

        map.addLayer({
            "id": "drone",
            "type": "symbol",
            "source": "drone",
            "layout": {
                "icon-image": "airport-15",
                "icon-rotation-alignment": "map"
            }
        });

        window.setInterval(setDronePos, 10);
    }
});

jQuery("#go-btn").click(function () {
    map.setCenter(drone.coordinates);
});

jQuery("#focus-btn").click(function () { //focuses on the marker
    if (focused === true) {
        focused = false;
        jQuery(this).removeClass("disabled");
    } else {
        focused = true;
        jQuery(this).addClass("disabled");
    }
});

joystickL.on("move", function (e, data) {
    joy_msg1.linear.x = +getAxisVal(data, "x");
    joy_msg1.angular.z = +getAxisVal(data, "y");
});

joystickR.on("move", function (e, data) {
    joy_msg2.linear.x = +getAxisVal(data, "x");
    joy_msg2.angular.z = +getAxisVal(data, "y");
});

joystickL.on("start", function (e) {
    joy_msg1.linear.x = +0.0;
    joy_msg1.angular.z = +0.0;
});

joystickR.on("start", function (e) {
    joy_msg2.linear.x = +0.0;
    joy_msg2.angular.z = +0.0;
});

joystickL.on("end", function (e) {
    joy_msg1.linear.x = +0.0;
    joy_msg1.angular.z = +0.0;
});

joystickR.on("end", function (e) {
    joy_msg2.linear.x = +0.0;
    joy_msg2.angular.z = +0.0;
});

function getAxisVal(data, axis){
        var force = data.force;
        var angle = data.angle.radian;
        var val = 0.0;
        if(axis === "x"){
            var tval = Math.cos(angle).toFixed(3);
            if(tval >= 0.1 || tval <= -0.1){
                val=tval;
            }
        }else if(axis === "y"){
            var tval = Math.sin(angle).toFixed(3);
            if(tval >= 0.1 || tval <= -0.1){
                val=tval;
            }
        }else{
            val = NaN;
        }
        return val;
}
function publishJoystics(){
        joystick_publisher1.publish(joy_msg1);
        joystick_publisher2.publish(joy_msg2);
        console.log(joy_msg1);
        console.log(joy_msg2);
}
    
    if (rosConnected) {


    }




//TODO Add list items and connect them to markers
//TODO Align the map and the info box - look at the columns
//TODO Draw linestrings in between the markers
//TODO Find a way to store array elements and save them into a file within the server

//TODO Make the waypoint markers draggable
