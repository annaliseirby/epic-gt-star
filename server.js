var express = require('express');
var app = express();
var port = process.env.PORT || 8081;
var path = require('path');
var bodyParser = require('body-parser');
var cookieParser = require('cookie-parser');
var session = require('express-session');

app.use(bodyParser());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, '/FrontEnd/static-content/')));

var firebase = require('firebase');

var pythonShell = require('python-shell');
var date = new Date();

var config = {
    apiKey: "AIzaSyDC5dkXYeRiKTTIonSlfUEy6OmKoYqRtKE",
    authDomain: "epicgtstar.firebaseapp.com",
    databaseURL: "https://epicgtstar.firebaseio.com",
    projectId: "epicgtstar",
    storageBucket: "epicgtstar.appspot.com",
    messagingSenderId: "141714341999"
};
firebase.initializeApp(config);

app.get('/', (req, res) => {
	var user = firebase.auth().currentUser;
	if (user) {
		res.sendFile(__dirname + '/FrontEnd/index.html');
	} else {
		res.redirect('/login');
	}
});

app.get('/login', (req, res) => {
	res.sendFile(__dirname + '/FrontEnd/login.html');
});

app.post('/login', (req, res) => {
	var userId = req.body.userID;
	var password = req.body.password;
	var email = userId + '@gatech.edu';
	firebase.auth().signInWithEmailAndPassword(email, password).then(() => {
		return res.redirect('/');
	}, (error) => {
		console.log(error.message);
		return res.redirect('/login');
	});
});

app.get('/logout', (req, res) => {
	firebase.auth().signOut();
	res.redirect('/login');
});

if (date.getHours() == 4 && date.getMinutes() == 20) {
	pythonShell.run(__dirname + '/BackEnd/Programs/UloopScraper.py');
	pythonShell.run(__dirname + '/BackEnd/Programs/HomeParkRentals.py');
}

app.listen(port);
console.log("Server running successfully on port 8081");