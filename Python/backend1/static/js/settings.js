const brightness =
document.getElementById("brightness");

const speed =
document.getElementById("speed");

brightness.oninput = () => {

document.getElementById(
"brightnessValue"
).innerHTML = brightness.value;

};

speed.oninput = () => {

document.getElementById(
"speedValue"
).innerHTML = speed.value;

};

document.getElementById(
"saveBtn"
).onclick = () => {

const settings = {

esp_ip:
document.getElementById("espIp").value,

brightness:
brightness.value,

speed:
speed.value,

led_count:
document.getElementById("ledCount").value

};

localStorage.setItem(
"holonova_settings",
JSON.stringify(settings)
);

document.getElementById(
"status"
).innerHTML =
"✅ Settings Saved Successfully";

};