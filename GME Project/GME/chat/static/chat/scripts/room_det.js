// ************************************** Room Date Conditional Start ************************************** //
// ************************************** Checks Room based on current day ************************************** //
var pathArray = window.location.pathname.split('/')
var d = new Date();
var weekday = new Array(7);
weekday[0] = "sun";
weekday[1] = "mon";
weekday[2] = "tues";
weekday[3] = "wed";
weekday[4] = "thurs";
weekday[5] = "fri";
weekday[6] = "sat";

var n = weekday[d.getDay()];
if (n != pathArray[2]) {
    // window.location.replace(window.location.protocol + "//" + window.location.host + "/");
    window.alert("Today is " + n + "day" + " you cannot enter this room, " + "\n" + "Please go to the right day of the week");
    window.location.replace("http://localhost:8000/chat/");
};
// ************************************** Room Date Conditional End ************************************** //

// ************************************** Room Playlist Conditional Start ************************************** //
// ******************************** Checks Spotify widget based on current path ******************************** //
// ******************************** And changes playlist according to schedule ******************************** //
if (document.location.pathname == '/rooms/sun/') {

    document.getElementById('spotify').src = 'https://open.spotify.com/embed/playlist/37i9dQZF1DX1lVhptIYRda'; 
};
if (document.location.pathname == '/rooms/mon/') {

    document.getElementById('spotify').src = 'https://open.spotify.com/embed/playlist/37i9dQZF1DWWQRwui0ExPn'; 
};
if (document.location.pathname == '/rooms/tues/') {

    document.getElementById('spotify').src = 'https://open.spotify.com/embed/playlist/37i9dQZF1DX0BcQWzuB7ZO'; 
};
if (document.location.pathname == '/rooms/wed/') {

    document.getElementById('spotify').src = 'https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M'; 
};
if (document.location.pathname == '/rooms/thurs/') {

    document.getElementById('spotify').src = 'https://open.spotify.com/embed/playlist/37i9dQZF1DX4FcAKI5Nhzq'; 
};
if (document.location.pathname == '/rooms/fri/') {

    document.getElementById('spotify').src = 'https://open.spotify.com/embed/playlist/37i9dQZF1DWVqJMsgEN0F4'; 
};
if (document.location.pathname == '/rooms/sat/') {

    document.getElementById('spotify').src = 'https://open.spotify.com/embed/playlist/37i9dQZF1DXcF6B6QPhFDv'; 
};
// ************************************** Room Playlist Conditional End ************************************** //