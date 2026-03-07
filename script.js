alert("JS LOADED")

// Camera access
let video = document.getElementById("video")

navigator.mediaDevices.getUserMedia({
    video: true
})
.then(stream => {
    video.srcObject = stream
})
.catch(err=>{
    console.log(err)
})

// GPS + Map
let lat
let lon
let map

navigator.geolocation.getCurrentPosition(function(pos){

    lat = pos.coords.latitude
    lon = pos.coords.longitude

    map = L.map("map").setView([lat, lon], 15)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19
    }).addTo(map)

    L.marker([lat, lon]).addTo(map)

})


// Capture Image + Send to API
function capture(){
  
  let canvas = document.getElementById("canvas")
  let ctx = canvas.getContext("2d")
  
  canvas.width = 400
  canvas.height = 300

  ctx.drawImage(video,0,0,400,300)

  let dataURL = canvas.toDataURL("image/jpeg")

  let formData = new FormData()

  formData.append("file", dataURItoBlob(dataURL), "capture.jpg")
  if (lat) formData.append("latitude", lat);
  if (lon) formData.append("longitude", lon);

  alert("API CALL START")

  fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    body: formData
  })
  .then(response => {
    console.log("RAW RESPONSE:", response)
    return response.text()
  })
  .then(text => {
    
    console.log("TEXT RESPONSE:", text)
    let data = JSON.parse(text)
    alert("API RESPONSE RECEIVED")
      
    let ndviValue = "N/A"
      
    if(data.ndvi && data.ndvi.nd){
      ndviValue = data.ndvi.nd
    }
    let resultHTML = "<h3>Analysis Result</h3>" +
    "<br>Status: " + data.status;
    
    if (data.reason) {
        resultHTML += "<br>Reason: " + data.reason;
    }
    
    resultHTML += 
    "<br>Latitude: " + (data.latitude || "N/A") +
    "<br>Longitude: " + (data.longitude || "N/A") +
    "<br>NDVI: " + ndviValue;

    if (data.crop_type) {
        resultHTML += "<br>Crop: " + data.crop_type + " (" + (data.confidence || 0) + "% confidence)";
    }
    if (data.damage_percentage !== undefined) {
        resultHTML += "<br>Damage: " + data.damage_percentage + "%";
    }
    if (data.loss_percentage !== undefined) {
        resultHTML += "<br>Estimated Loss: " + data.loss_percentage + "%";
    }
    if (data.map_url) {
        resultHTML += "<br><a href='" + data.map_url + "' target='_blank'>View on Map</a>";
    }

    document.getElementById("result").innerHTML = resultHTML;
  })
  .catch(error => {
    console.log("FETCH ERROR:", error)
    alert("Error: " + error.message)
  })

}

function dataURItoBlob(dataURI) {
    let byteString = atob(dataURI.split(',')[1]);
    let mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    let ab = new ArrayBuffer(byteString.length);
    let ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], {type: mimeString});
}