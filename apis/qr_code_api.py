import qrcode
import qrcode.image.svg
import io
from flask_restplus import Namespace, Resource, reqparse, marshal, fields
from flask import make_response, jsonify

from models.authorization import authorize_decorator

api = Namespace('QR', description='QR-code api.')


qr_code_object = api.model(name='qr-code-object', model={
    'value': fields.String,
    'qr_code': fields.String,
})
# qr_code_response = api.model(name='qr-code-array', model={
#     'qr_codes': fields.List(fields.Nested(qr_code_object)),
# })


@api.route('')
class QRApi(Resource):
    method_decorators = [authorize_decorator]

    @api.expect([qr_code_object], validate=False)
    @api.response(200, 'Success', [qr_code_object])
    def post(self):
        factory = qrcode.image.svg.SvgImage
        QR_codes = []
        text_values = api.payload
        print(text_values)

        for value in text_values:
            qr_code_image = qrcode.make(value, image_factory=factory)
            bytes_file = io.BytesIO()
            qr_code_image.save(bytes_file)
            bytes_file.seek(0)
            byte_str = bytes_file.read()
            str_svg = byte_str.decode('utf-8')
            QR_codes.append({'value': value, 'qr_code': str_svg})
        # response = {'qr_codes': QR_codes}
        return QR_codes
