from flask import Flask
from flask import request
from flask import jsonify
from bus import Bus
from InvalidParameterException import InvalidParameterException

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1>Hello World</h1>'


@app.route('/bus/<router_name>/stop/<stop_id>')
def query_stop(router_name, stop_id):
    direction = request.args.get('direction', '0')

    bus = Bus()
    res = bus.query_stop(router_name, direction, stop_id)

    return jsonify(res)


@app.route('/bus/<router_name>')
def query_router(router_name):
    direction = request.args.get('direction', '0')

    bus = Bus()
    routers = bus.query_router(router_name, direction)

    return jsonify(routers)


@app.route('/bus/<router_name>/details')
def query_router_details(router_name):
    direction = request.args.get('direction', '0')

    bus = Bus()
    router_details = bus.query_router_details(router_name, direction)

    return jsonify(router_details)


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'not_found',
        'error_msg': '链接不存在'
    }), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'error': 'internal_server_error',
        'error_msg': '服务器内部错误'
    }), 500


@app.errorhandler(InvalidParameterException)
def handle_invalid_parameter(e):
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port=8080, debug=False, threaded=True)
