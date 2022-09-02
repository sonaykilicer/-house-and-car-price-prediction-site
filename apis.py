from importlib.resources import Resource
from flask import request
from flask_restful import Resource
import pandas as pd
import housePricePredictionModel
import carPricePredictionModel
import jsonify

class HousePricePredictionApi(Resource):

    def get(self):


        args = request.args

        ilce = int(args['ilce'])
        net = int(args['net'])
        brut = int(args['brut'])
        oda = int(args['oda'])
        yas = int(args['yas'])
        kat = int(args['kat'])

        yeni_veri = [[ilce], [net], [brut], [oda], [yas], [kat]]    
        yeni_veri = pd.DataFrame(yeni_veri).T

        df_2 = yeni_veri.rename(columns = {0:"İlce",
                            1:"brüt metrekare",
                            2:"Net Metrekare",
                            3:"Oda Sayısı",
                            4:"Binanın Yaşı",
                            5:"Bulunduğu Kat"})

        pred = housePricePredictionModel.model_xgb.predict(df_2)

        return str(pred) 

class CarPricePredictionApi(Resource):

    def get(self):

        args = request.args

        marka = int(args['marka'])
        seri = int(args['seri'])
        yil = int(args['yil'])
        yakit = int(args['yakit'])
        vites = int(args['vites'])
        motorh = int(args['motor_hacmi'])
        motorg = int(args['motor_gucu'])
        km = int(args['km'])
        tramer = int(args['tramer'])

        yeni_veri = [[marka], [seri], [yil], [yakit], [vites], [motorh], [motorg], [km], [tramer]]
        yeni_veri = pd.DataFrame(yeni_veri).T
        
        df_2 = yeni_veri.rename(columns = {0:"Marka",
                            1:"Seri",
                            2:"Yıl",
                            3:"Yakıt Tipi",
                            4:"Vites Tipi",
                            5:"Motor Hacmi",
                            6:"Motor Gücü",
                            7:"Kilometre",
                            8:"Toplam Tramer Tutarı"})

        pred = carPricePredictionModel.model_xgb.predict(df_2)
    
        return str(pred)