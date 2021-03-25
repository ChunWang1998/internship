from flask import Flask, abort
from flask import jsonify
from google.cloud import storage
from google.oauth2 import service_account
app = Flask(__name__)


COLOR = ['black', 'white', 'green', 'red']
SHAPE = ['triangle', 'circle', 'rectangle']
FAVORITE_FOOD = ['hamburger','cola','rice','pop corn']
HOMETOWN = ['US','JAPAN','KOREA','TAIWAN']

@app.route('/api/creature/<token_id>')
def creature(token_id):
    token_id = int(token_id)
    creature_name = 'Joe monster' + str(token_id)

    #image_url = 'https://github.com/ChunWang1998/opensea_puipui_car/blob/main/CCar.jpeg'
    image_url = 'https://storage.googleapis.com/opensea-prod.appspot.com/puffs/' + str(token_id%20)+'.png'

    attributes = []
    _add_attribute(attributes, 'color', COLOR, token_id)
    _add_attribute(attributes, 'shape', SHAPE, token_id)
    _add_attribute(attributes, 'favorite food', FAVORITE_FOOD, token_id)
    _add_attribute(attributes, 'hometown', HOMETOWN, token_id)



    return jsonify({
        'name': creature_name,
        'description': 'Monster tested by Joe ',
        'image': image_url,
        #'external_url': 'https://openseacreatures.io/%s' % token_id,
        'attributes': attributes
    })


def _add_attribute(existing, attribute_name, options, token_id, display_type=None):
    trait = {
        'trait_type': attribute_name,
        'value': options[token_id % len(options)]
    }
    if display_type:
        trait['display_type'] = display_type
    existing.append(trait)


# Error handling

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, use_reloader=True)
