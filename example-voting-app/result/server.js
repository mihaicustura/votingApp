var express = require('express'),
    async = require('async'),
    pg = require("pg"),
    path = require("path"),
    cookieParser = require('cookie-parser'),
    bodyParser = require('body-parser'),
    methodOverride = require('method-override'),
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server);

io.set('transports', ['polling']);

var port = process.env.PORT || 4000;

io.sockets.on('connection', function (socket) {

  socket.emit('message', { text : 'Welcome!' });

  socket.on('subscribe', function (data) {
    socket.join(data.channel);
  });
});

async.retry(
  {times: 1000, interval: 1000},
  function(callback) {
    pg.connect('postgres://postgres@db/postgres', function(err, client, done) {
      if (err) {
        console.error("Waiting for db");
      }
      callback(err, client);
    });
  },
  function(err, client) {
    if (err) {
      return console.error("Giving up");
    }
    console.log("Connected to db");
    getVotes(client);
  }
);

function getVotes(client) {
  //client.query('SELECT "AXWELL ^ INGROSSO" as vote, COUNT(id) AS count FROM votes GROUP BY "AXWELL ^ INGROSSO"', [], function(err, result) {
    client.query('SELECT * from votes', [], function(err, result) {
    if (err) {
      console.error("Error performing query: " + err);
    } else {
      var votes = collectVotesFromResult(result);
      io.sockets.emit("scores", JSON.stringify(votes));
      //console.log(JSON.stringify(votes));
    }

    setTimeout(function() {getVotes(client) }, 1000);
  });
}

function collectVotesFromResult(result) {
  var votes = {"ARMIN VAN BUUREN": 0, "AXWELL ^ INGROSSO": 0, "HARDWELL": 0, "JOHN NEWMAN": 0, "STEVE ANGELLO": 0, "STEVE AOKI": 0, "THE SCRIPT": 0, "ALAN WALKER": 0, "GALANTIS": 0, "GTA": 0, "JONAS BLUE": 0, "KUNGS": 0, "REDFOO": 0, "SCOOTER": 0, "SUBCARPATI": 0, "SUNNERY JAMES & RYAN MARCIANO": 0, "TUJAMO": 0, "W&W": 0, "YELLOW CLAW": 0, "JAMIE JONES": 0, "NINA KRAVIZ": 0, "AME DJ": 0, "CEZAR": 0, "EATS EVERYTHING": 0, "PRASLEA": 0, "PRIKU": 0, "RARESH": 0, "SIT": 0, "CHARLIE": 0, "DAN ANDREI": 0, "EMI": 0, "KOZO": 0, "LUCY": 0, "MUMDANCE": 0, "PAUL AGRIPA": 0, "PREMIESKU": 0, "SUBLEE": 0, "VINCENTIULIAN": 0, "CAMO & KROOKED": 0, "CHASE & STATUS": 0, "DJ PREMIER": 0, "DOPE D.O.D": 0, "DUB FX": 0, "MODESTEP": 0, "NGHTMRE": 0, "NOISIA": 0, "PENDULUM": 0, "RUSKO": 0, "CULESE DIN CARTIER": 0, "DOC": 0, "DELIRIC & SILENT STRIKE": 0, "GRASU XXL": 0, "MACANACHE": 0, "PARAZITII": 0, "SATRA B.E.N.Z.": 0, "ACID PAULI": 0, "BEGUN": 0, "BLACK COFFEE": 0, "BLOND:ISH": 0, "CHRISTIAN LOFLER": 0, "CLAPTONE": 0, "EL MUNDO": 0, "HOLMAR": 0, "JAN BLOMQVIST & BAND": 0, "KERALA DUST": 0, "LUM": 0, "MARWAN": 0, "NIGHTMARES ON WAX": 0, "NU": 0, "RAMPUE": 0, "SATORI": 0, "STAVROZ": 0, "VIKEN ARMAN": 0, "YOKOO": 0};

  result.rows.forEach(function (row) {
    for (var vote in votes) {
	if (row.vote.includes(vote)) {
		votes[vote]++;
	}
    }
  });

  return votes;
}

app.use(cookieParser());
app.use(bodyParser());
app.use(methodOverride('X-HTTP-Method-Override'));
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header("Access-Control-Allow-Methods", "PUT, GET, POST, DELETE, OPTIONS");
  next();
});

app.use(express.static(__dirname + '/views'));

app.get('/', function (req, res) {
  res.sendFile(path.resolve(__dirname + '/views/index.html'));
});

server.listen(port, function () {
  var port = server.address().port;
  console.log('App running on port ' + port);
});
