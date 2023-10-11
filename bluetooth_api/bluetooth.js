document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("btn");
    btn.addEventListener('click', async function () {
        navigator.bluetooth.requestDevice({ filters: [{
            name: 'GoPro 8370'
        }],
        optionalServices: ['battery_service'] // Required to access service later.
    }) 
        .then(device => device.gatt.connect())
        .then(server => {
        // Getting Battery Service…
        return server.getPrimaryService('battery_service');
        })
        .then(service => {
        // Getting Battery Level Characteristic…
        return service.getCharacteristic('battery_level');
        })
        .then(characteristic => {
        // Reading Battery Level…
        return characteristic.readValue();
        })
        .then(value => {
        console.log(value)
        console.log(`Battery percentage is ${value.getUint8(0)}`);
        })
        .catch(error => { console.error(error); });
      });

    
})



const enableWifi = async() => {
    const uuid = "b5f9XXXX-aa8d-11e3-9046-0002a5d5c51b";
    const command_req_uuid = uuid.replace("XXXX", "0072")
    const command_rsp_uuid = uuid.replace("XXXX", "0073")
    const wifi_ap_uuid = uuid.replace("XXXX", "0002")
    const wifi_psw_uuid = uuid.replace("XXXX", "0003")
    try {
    const device = await navigator.bluetooth.requestDevice({
        filters: [{
            name: 'GoPro 8370'
        }],
        optionalServices: ['battery_service'] // Required to access service later.
        })
    console.log(device.name);
    const connectDevice = await device.gatt.connect();
    console.log(connectDevice);
    
    // const reqCharacteristic = await connectDevice.getPrimaryService(command_rsp_uuid)
    const ssid = await connectDevice.getPrimaryService('battery_service').getCharacteristic('battery_level').readValue()
    console.log(`Battery percentage is ${ssid.getUint8(0)}`);

    }
    catch{
        error => {console.error(error)}
    }
}