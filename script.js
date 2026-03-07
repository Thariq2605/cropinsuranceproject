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

  alert("API CALL START")

  fetch("http://127.0.0.1:9000/analyze", {
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
    document.getElementById("result").innerHTML =
    "<h3>Analysis Result</h3>" +
    "<br>Status: " + data.status +
    "<br>Latitude: " + data.latitude +
    "<br>Longitude: " + data.longitude +
    "<br>NDVI: " + ndviValue
  })
  .catch(error => {
    console.log("FETCH ERROR:", error)
  })

}