from flask import request
from flask import Flask, render_template, redirect
from flask_restful import Api, Resource
import apis

app = Flask(__name__)

api = Api(app)

#API
api.add_resource(apis.HousePricePredictionApi, '/housePredict')
api.add_resource(apis.CarPricePredictionApi, '/carPredict')

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/house", methods = ['POST', 'GET'])
def house():
        if request.method == 'GET':
                return render_template("house.html")
        if request.method == 'POST':
                district = request.form.get('district_select')
                gross = request.form['gross_msquare']
                net = request.form['net_msquare']
                room = request.form.get('room_select')
                age = request.form.get('building_age')
                floor = request.form.get('floor_loc')
                #[ilce], [net], [brut], [oda], [yas], [kat]] 
                url = 'housePredict?ilce=' + district + '&brut=' + gross + '&net='
                + net + '&oda=' + room + '&yas=' + age + '&kat=' + floor
                return redirect(url)

@app.route("/car", methods = ['POST', 'GET'])
def car():
        if request.method == 'GET':
                return render_template("car.html")
        if request.method == 'POST':
                brand = request.form.get('brand_select')
                model = request.form.get('model_select')
                year = request.form['year']
                fuel = request.form.get('fuel_select')
                gear = request.form.get('gear_select')
                engineCapacity = request.form['engineCapacity']
                motorPower = request.form['motorPower']
                kilometer = request.form['kilometer']
                accident = request.form['accident']
                url = "/carPredict?marka=" + brand + "&seri=" + model +"&yil=" 
                + year + "&yakit=" + fuel + "&vites=" + gear + "&motor_hacmi=" 
                + engineCapacity + "&motor_gucu=" + motorPower + "&km=" + kilometer + "&tramer=" + accident
                return redirect(url)   

if __name__ == "__main__":
    app.run(debug=True)