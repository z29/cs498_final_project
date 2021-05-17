var server_port = 65432;
var server_addr = "192.168.1.42";   // the IP address of your Raspberry PI
var outer_open = false;
var inner_open = false;
var light_1_on = false;
var light_2_on = false;
var light_3_on = false;

var airlock_warning = "WARNING!!! OTHER AIRLOCK MUST BE CLOSED"

function client(input){
    
    const net = require('net');

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        document.getElementById("greet_from_server").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

function greeting(){

    // get the element from html
    var name = document.getElementById("myName").value;
    // update the content in html
    document.getElementById("greet").innerHTML = "Hello " + name + " !";
    // send the data to the server 
    client();

}

function outer_airlock(){
    if(inner_open){
        alert(airlock_warning)
    }else{
        client("1")
        outer_open = !outer_open
        if(outer_open){
            document.getElementById("outer_airlock").innerHTML = "OPEN";
        } else{
            document.getElementById("outer_airlock").innerHTML = "CLOSED";
        }
    }
}

function inner_airlock(){
    if(outer_open){
        alert(airlock_warning)
    }else{
        client("2")
        inner_open = !inner_open
        if(inner_open){
            document.getElementById("inner_airlock").innerHTML = "OPEN";
        } else{
            document.getElementById("inner_airlock").innerHTML = "CLOSED";
        }
    }
}

function light_1(){
    client("5")
    light_1_on = !light_1_on
    if(light_1_on){
        document.getElementById("light_1").innerHTML = "ON";
    } else{
        document.getElementById("light_1").innerHTML = "OFF";
    }
}

function light_2(){
    client("6")
    light_2_on = !light_2_on
    if(light_2_on){
        document.getElementById("light_2").innerHTML = "ON";
    } else{
        document.getElementById("light_2").innerHTML = "OFF";
    }
}

function light_3(){
    client("7")
    light_3_on = !light_3_on
    if(light_3_on){
        document.getElementById("light_3").innerHTML = "ON";
    } else{
        document.getElementById("light_3").innerHTML = "OFF";
    }
}

