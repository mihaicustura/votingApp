from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json

option1 = os.getenv('OPTION1', "ARMIN VAN BUUREN")
option2 = os.getenv('OPTION2', "AXWELL ^ INGROSSO")
option3 = os.getenv('OPTION3', "HARDWELL")
option4 = os.getenv('OPTION4', "JOHN NEWMAN")
option5 = os.getenv('OPTION5', "STEVE ANGELLO")
option6 = os.getenv('OPTION6', "STEVE AOKI")
option7 = os.getenv('OPTION7', "THE SCRIPT")
option8 = os.getenv('OPTION8', "ALAN WALKER")
option9 = os.getenv('OPTION9', "GALANTIS")
option10 = os.getenv('OPTION10', "GTA")
option11 = os.getenv('OPTION11', "JONAS BLUE")
option12 = os.getenv('OPTION12', "KUNGS")
option13 = os.getenv('OPTION13', "REDFOO")
option14 = os.getenv('OPTION14', "SCOOTER")
option15 = os.getenv('OPTION15', "SUBCARPATI")
option16 = os.getenv('OPTION16', "SUNNERY JAMES & RYAN MARCIANO")
option17 = os.getenv('OPTION17', "TUJAMO")
option18 = os.getenv('OPTION18', "W&W")
option19 = os.getenv('OPTION19', "YELLOW CLAW")


option20 = os.getenv('OPTION20', "JAMIE JONES")
option21 = os.getenv('OPTION21', "NINA KRAVIZ")
option22 = os.getenv('OPTION22', "AME DJ")
option23 = os.getenv('OPTION23', "CEZAR")
option24 = os.getenv('OPTION24', "EATS EVERYTHING")
option25 = os.getenv('OPTION25', "PRASLEA")
option26 = os.getenv('OPTION26', "PRIKU")
option27 = os.getenv('OPTION27', "RARESH")
option28 = os.getenv('OPTION28', "SIT")
option29 = os.getenv('OPTION29', "CHARLIE")
option30 = os.getenv('OPTION30', "DAN ANDREI")
option31 = os.getenv('OPTION31', "EMI")
option32 = os.getenv('OPTION32', "KOZO")
option33 = os.getenv('OPTION33', "LUCY")
option34 = os.getenv('OPTION34', "MUMDANCE")
option35 = os.getenv('OPTION35', "PAUL AGRIPA")
option36 = os.getenv('OPTION36', "PREMIESKU")
option37 = os.getenv('OPTION37', "SUBLEE")
option38 = os.getenv('OPTION38', "VINCENTIULIAN")

option39 = os.getenv('OPTION39', "CAMO & KROOKED")
option40 = os.getenv('OPTION40', "CHASE & STATUS")
option41 = os.getenv('OPTION41', "DJ PREMIER")
option42 = os.getenv('OPTION42', "DOPE D.O.D")
option43 = os.getenv('OPTION43', "DUB FX")
option44 = os.getenv('OPTION44', "MODESTEP")
option45 = os.getenv('OPTION45', "NGHTMRE")
option46 = os.getenv('OPTION46', "NOISIA")
option47 = os.getenv('OPTION47', "PENDULUM")
option48 = os.getenv('OPTION48', "RUSKO")
option49 = os.getenv('OPTION49', "CULESE DIN CARTIER")
option50 = os.getenv('OPTION50', "DOC")
option51 = os.getenv('OPTION51', "DELIRIC & SILENT STRIKE")
option52 = os.getenv('OPTION52', "GRASU XXL")
option53 = os.getenv('OPTION53', "MACANACHE")
option54 = os.getenv('OPTION54', "PARAZITII")
option55 = os.getenv('OPTION55', "SATRA B.E.N.Z.")

option56 = os.getenv('OPTION56', "ACID PAULI")
option57 = os.getenv('OPTION57', "BEGUN")
option58 = os.getenv('OPTION58', "BLACK COFFEE")
option59 = os.getenv('OPTION59', "BLOND:ISH")
option60 = os.getenv('OPTION60', "CHRISTIAN LOFLER")
option61 = os.getenv('OPTION61', "CLAPTONE")
option62 = os.getenv('OPTION62', "EL MUNDO")
option63 = os.getenv('OPTION63', "HOLMAR")
option64 = os.getenv('OPTION64', "JAN BLOMQVIST & BAND")
option65 = os.getenv('OPTION65', "KERALA DUST")
option66 = os.getenv('OPTION66', "LUM")
option67 = os.getenv('OPTION67', "MARWAN")
option68 = os.getenv('OPTION68', "NIGHTMARES ON WAX")
option69 = os.getenv('OPTION69', "NU")
option70 = os.getenv('OPTION70', "RAMPUE")
option71 = os.getenv('OPTION71', "SATORI")
option72 = os.getenv('OPTION72', "STAVROZ")
option73 = os.getenv('OPTION73', "VIKEN ARMAN")
option74 = os.getenv('OPTION74', "YOKOO")
hostname = socket.gethostname()

app = Flask(__name__)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option1=option1,
        option2=option2,
	option3=option3,
	option4=option4,
	option5=option5,
	option6=option6,
	option7=option7,
	option8=option8,
	option9=option9,
	option10=option10,
	option11=option11,
	option12=option12,
	option13=option13,
	option14=option14,
	option15=option15,
	option16=option16,
	option17=option17,
	option18=option18,
	option19=option19,
        option20=option20,
        option21=option21,
	option22=option22,
	option23=option23,
	option24=option24,
	option25=option25,
	option26=option26,
	option27=option27,
	option28=option28,
	option29=option29,
	option30=option30,
	option31=option31,
	option32=option32,
	option33=option33,
	option34=option34,
	option35=option35,
	option36=option36,
	option37=option37,
	option38=option38,
	option39=option39,
	option40=option40,
	option41=option41,
	option42=option42,
	option43=option43,
	option44=option44,
	option45=option45,
	option46=option46,
	option47=option47,
	option48=option48,
	option49=option49,
	option50=option50,
	option51=option51,
	option52=option52,
	option53=option53,
	option54=option54,
	option55=option55,
	option56=option56,
	option57=option57,
	option58=option58,
	option59=option59,
	option60=option60,
	option61=option61,
	option62=option62,
	option63=option63,
	option64=option64,
	option65=option65,
	option66=option66,
	option67=option67,
	option68=option68,
	option69=option69,
	option70=option70,
	option71=option71,
	option72=option72,
	option73=option73,
	option74=option74,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

@app.route("/new", methods=['POST','GET'])
def new():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = ""

    if request.method == 'POST':
        redis = get_redis()
        #vote = request.form['vote']
	votes = request.form.items()
	for v in votes:
		vote += v[0] + ","
	vote = vote[:-1]
	#vote = option1 + " " + request.form[option1] + " " + option2 + " " + request.form[option2] + " " + option3 + " " + request.form[option3] + " " + option4 + " " + request.form[option4] + " " + option5 + " " + request.form[option5] + " " + option6 + " " + request.form[option6] + " " + option7 + " " + request.form[option7] + " " + option8 + " " + request.form[option8] + " " + option9 + " " + request.form[option9] + " " + option10 + " " + request.form[option10] + " " + option11 + " " + request.form[option11] + " " + option12 + " " + request.form[option12] + " " + option13 + " " + request.form[option13] + " " + option14 + " " + request.form[option14] + " " + option15 + " " + request.form[option15] + " " + option16 + " " + request.form[option16] + " " + option17 + " " + request.form[option17] + " " + option18 + " " + request.form[option18] + " " + option19 + " " + request.form[option19] + " " + option20 + " " + request.form[option20] + " " + option21 + " " + request.form[option21] + " " + option22 + " " + request.form[option22] + " " + option23 + " " + request.form[option23] + " " + option24 + " " + request.form[option24] + " " + option25 + " " + request.form[option25] + " " + option26 + " " + request.form[option26] + " " + option27 + " " + request.form[option27] + " " + option28 + " " + request.form[option28] + " " + option29 + " " + request.form[option29] + " " + option30 + " " + request.form[option30] + " " + option31 + " " + request.form[option31] + " " + option32 + " " + request.form[option32] + " " + option33 + " " + request.form[option33] + " " + option34 + " " + request.form[option34] + " " + option35 + " " + request.form[option35] + " " + option36 + " " + request.form[option36] + " " + option37 + " " + request.form[option37] + " " + option38 + " " + request.form[option38] + " " + option39 + " " + request.form[option39] + " " + option40 + " " + request.form[option40] + " " + option41 + " " + request.form[option41] + " " + option42 + " " + request.form[option42] + " " + option43 + " " + request.form[option43] + " " + option44 + " " + request.form[option44] + " " + option45 + " " + request.form[option45] + " " + option46 + " " + request.form[option46] + " " + option47 + " " + request.form[option47] + " " + option48 + " " + request.form[option48] + " " + option49 + " " + request.form[option49] + " " + option50 + " " + request.form[option50] + " " + option51 + " " + request.form[option51] + " " + option52 + " " + request.form[option52] + " " + option53 + " " + request.form[option53] + " " + option54 + " " + request.form[option54] + " " + option55 + " " + request.form[option55] + " " + option56 + " " + request.form[option56] + " " + option57 + " " + request.form[option57] + " " + option58 + " " + request.form[option58] + " " + option59 + " " + request.form[option59] + " " + option60 + " " + request.form[option60] + " " + option61 + " " + request.form[option61] + " " + option62 + " " + request.form[option62] + " " + option63 + " " + request.form[option63] + " " + option64 + " " + request.form[option64] + " " + option65 + " " + request.form[option65] + " " + option66 + " " + request.form[option66] + " " + option67 + " " + request.form[option67] + " " + option68 + " " + request.form[option68] + " " + option69 + " " + request.form[option69] + " " + option70 + " " + request.form[option70] + " " + option71 + " " + request.form[option71] + " " + option72 + " " + request.form[option72] + " " + option73 + " " + request.form[option73] + " " + option74 + " " + request.form[option74]
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
	print data
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option1=option1,
        option2=option2,
	option3=option3,
	option4=option4,
	option5=option5,
	option6=option6,
	option7=option7,
	option8=option8,
	option9=option9,
	option10=option10,
	option11=option11,
	option12=option12,
	option13=option13,
	option14=option14,
	option15=option15,
	option16=option16,
	option17=option17,
	option18=option18,
	option19=option19,
        option20=option20,
        option21=option21,
	option22=option22,
	option23=option23,
	option24=option24,
	option25=option25,
	option26=option26,
	option27=option27,
	option28=option28,
	option29=option29,
	option30=option30,
	option31=option31,
	option32=option32,
	option33=option33,
	option34=option34,
	option35=option35,
	option36=option36,
	option37=option37,
	option38=option38,
	option39=option39,
	option40=option40,
	option41=option41,
	option42=option42,
	option43=option43,
	option44=option44,
	option45=option45,
	option46=option46,
	option47=option47,
	option48=option48,
	option49=option49,
	option50=option50,
	option51=option51,
	option52=option52,
	option53=option53,
	option54=option54,
	option55=option55,
	option56=option56,
	option57=option57,
	option58=option58,
	option59=option59,
	option60=option60,
	option61=option61,
	option62=option62,
	option63=option63,
	option64=option64,
	option65=option65,
	option66=option66,
	option67=option67,
	option68=option68,
	option69=option69,
	option70=option70,
	option71=option71,
	option72=option72,
	option73=option73,
	option74=option74,
        hostname=hostname,
        #vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
