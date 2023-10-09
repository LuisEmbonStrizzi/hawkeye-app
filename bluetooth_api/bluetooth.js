document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("btn");
    btn.addEventListener('click', function() {
        navigator.bluetooth.requestDevice({ filters: [{
            name: 'GoPro 8370'
        }], })
        .then(device => {
        // Human-readable name of the device.
        console.log(device.name);

        // Attempts to connect to remote GATT Server.
        return device.gatt.connect();
        })
        .then(server => { console.log(server)})
        .catch(error => { console.error(error); });
      });
    
})



const enableWifi = async() => {
    try {
    const device = await (navigator.bluetooth.requestDevice({
        filters: [{
            name: 'GoPro 8370'
        }],
        optionalServices: ['battery_service'] // Required to access service later.
        }))
    console.log(device.name);
    const connectDevice = await device.gatt.connect();
    console.log(connectDevice);
    }
    catch{
        error => {console.error(error)}
    }
}