from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import uuid
from database import Staff
import config

app = Flask(__name__, static_url_path="/images")
CORS(app)

ADDRESS = config.ADDRESS


@app.route('/', methods=['GET'])
def hello():
    if request.method == 'GET':
        return jsonify({'message': 'test'}), 200


@app.route('/avatar/<staff_id>', methods=['POST'])
def avatar(staff_id):
    if request.method == 'POST':
        user = Staff.get_or_none(Staff.id == staff_id)
        if user is None:
            return jsonify({'message': 'staff_id does not exist'}), 403
        if 'files[]' not in request.files:
            return jsonify({'message': 'No file part in the request'}), 422
        files = request.files.getlist('files[]')
        errors = {}
        success = False
        for file in files:
            if not os.path.exists(config.AVATAR_UPLOAD_FOLDER + '/' + staff_id):
                os.makedirs(config.AVATAR_UPLOAD_FOLDER + '/' + staff_id)
            if file:
                filename = (uuid.uuid4().hex)[0:10] + datetime.now().strftime('%Y%m%d%H%M%S') + '.webp'
                file.save(os.path.join(config.AVATAR_UPLOAD_FOLDER + '/' + staff_id, filename))
                road = config.AVATAR_UPLOAD_ALIAS + '/' + staff_id + '/' + filename
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'
        if success and errors:
            errors['message'] = 'something wrong'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
        if success:
            user = Staff(photo=road)
            user.id = staff_id
            user.save()
            return jsonify({'message': 'success', 'image': road}), 200
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
