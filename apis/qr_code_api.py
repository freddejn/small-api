import qrcode
import qrcode.image.svg
import io
from flask_restplus import Namespace, Resource, fields

from models.authorization import authorize_decorator

api = Namespace('QR', description='QR-code api.')


qr_code_object = api.model(name='QR-code', model={
    'value': fields.String(
        description='QR-code will be created from this value, \
             link, value etc.'),
    'qr_code': fields.String(description='SVG QR-code as a string.'),
})


@api.route('')
class QRApi(Resource):
    method_decorators = [authorize_decorator]

    @api.expect([qr_code_object], validate=False)
    @api.response(200, 'Success', [qr_code_object])
    def post(self):
        factory = qrcode.image.svg.SvgImage
        QR_codes = []
        text_values = api.payload

        for qr_code in text_values:
            qr_code_image = qrcode.make(
                qr_code['value'], image_factory=factory)
            bytes_file = io.BytesIO()
            qr_code_image.save(bytes_file)
            bytes_file.seek(0)
            byte_str = bytes_file.read()
            str_svg = byte_str.decode('utf-8')
            qr_code['qr_code'] = str_svg
            QR_codes.append(qr_code)
        return QR_codes
