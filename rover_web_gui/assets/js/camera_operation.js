$(document).ready(function () {
    $("#set-cam-ip").on("click", function () {
        var adr1 = "http://" + $("#cam-url-1").val();
        var adr2 = "http://" + $("#cam-url-2").val();
        var adr3 = "http://" + $("#cam-url-3").val();
        var adr4 = "http://" + $("#cam-url-4").val();
        var adr5 = "http://" + $("#cam-url-5").val();
        console.log(adr1);
        console.log(adr2);
        console.log(adr3);
        
        $("#cam1-port").attr("src", adr1);
        $("#cam2-port").attr("src", adr2);
        $("#cam3-port").attr("src", adr3);
        $("#cam4-port").attr("src", adr4);
        $("#cam5-port").attr("src", adr5);
    });
});