#SGLSim_Basic/app.py
from flask import Flask, render_template, jsonify, request
import redis
import math
import json

r = redis.Redis()
app = Flask(__name__)

app.secret_key = "caircocoders-ednalan"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/postskill",methods=["POST","GET"])
def postskill():
    if request.method == 'POST':
        name = request.form.get('request_name')
        location = request.form.get('weather_file')
        hvac =  request.form.get('hvac_type')
        daylight_control = request.form.get('daylight_control')
        building_type = request.form.get('building_type')
        blind_control = request.form.get('blind_type')
        length = math.floor(math.sqrt(int(request.form.get('len'))))
        height = request.form.get('height')
        wwrmax = request.form.get('wwr_max')
        wwrmin = request.form.get('wwr_min')
        wwrincremen = request.form.get('len_wwr')
        min_orientation = request.form.get('min_orientation')
        max_orientation = request.form.get('max_orientation')
        len_orientation = request.form.get('len_orientation')
        shgc = request.form.getlist('shgc[]')
        uvalue = request.form.getlist('uvalue[]')
        vlt = request.form.getlist('vlt[]')
        # email = current_user.email
        pv = request.form.getlist('pv[]')
        wwr = []
        i = int(wwrmin)
        j = int(wwrmax)
        k = int(wwrincremen)
        inc = int(wwrmax)/int(wwrincremen)
        while i<=j:
            wwr.append(i)
            i = i + int(inc)
        orientation = []
        x = int(min_orientation)
        y = int(max_orientation)
        incDirection = int(max_orientation)/int(len_orientation)
        while x<y:
            orientation.append(x)
            x = x + int(incDirection)

        print(  f' Building Name is {name} and has HVAC {hvac}'
                f' Simulation location is {location} &'
                f' Orientation is {orientation}'
                f' WWR is {wwr}'
                f' Length, Height is as follows {length}, {height}'
                f' Daylighting Control is {daylight_control}'
                f' Building Type is {building_type}'
                f' Blind Control is {blind_control}'
                f' SHGC is {shgc}'
                f' UValue is {uvalue}'
                f' VLT is {vlt}')

        r.lpush('queue',json.dumps({
            'name': name,
            'location': location,
            'hvac': hvac,
            'daylight_control': daylight_control,
            'building_type': building_type,
            'blind_control': blind_control,
            'length': length,
            'height': height,
            'wwr': wwr,
            'orientation': orientation,
            'shgc' : shgc,
            'uvalue': uvalue,
            'vlt': vlt,
            'pv' : pv,
                }))
        msg = 'New record created successfully'
    return jsonify(msg)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
