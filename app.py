#!/usr/bin/python3
from flask import Flask, request, jsonify

from action import ActionThread

app = Flask(__name__)


@app.route('/led/<led_id>', methods=['POST'])
def led(led_id):
    """
    request parameters:
    - on: % of the time the led should stay on.
    - freq: Frequency in Hz to which the led should be on.
    - delay: Delay in seconds before executing the request.

    Example:
    - To turn on the led: on=100
    - To turn off the led in 2 seconds: on=0, delay=2
    - To blink the led every second: on=50, freq=1
    - To blink the led every 10 seconds with 8 seconds on: on=80, freq=0.1

    :param led_id: GPIO on the raspberry pi
    :return:
    """
    # Gets parameters
    delay = request.args.get('delay', 0, int)
    on = request.args.get('on', 0, int)
    freq = request.args.get('freq', 0, float)

    # Validates parameters
    validate(delay, freq, on)

    # Executes action with optional delay
    if delay == 0:
        ActionThread(led_id, delay, on, freq).run()
    else:
        ActionThread(led_id, delay, on, freq).start()

    return build_response(led_id, delay, on, freq)


class BadRequestError(ValueError):
    pass


@app.errorhandler(BadRequestError)
def bad_request_handler(error):
    return bad_request(error.args[0])


def bad_request(message):
    response = build_message(message)
    response.status_code = 400
    return response


def build_message(message):
    return jsonify({'message': message})


def validate(delay, freq, on):
    if delay < 0:
        raise BadRequestError(f'delay should be positive ({delay})')
    if on < 0 or on > 100:
        raise BadRequestError(f'on should be a percentage ({on})')
    if 0 < on < 100 and freq <= 0:
        raise BadRequestError(f'freq should be strictly positive ({freq})')


def build_response(led_id, delay, on, freq):
    delay_str = ""
    if delay > 0:
        delay_str = f' in {delay} second(s)'

    if on == 0:
        return build_message(f'Turn off led {led_id}{delay_str}')
    elif on == 100:
        return build_message(f'Turn on led {led_id}{delay_str}')
    else:
        return build_message(f'blink led {led_id} with freq {freq} Hz at {on} %{delay_str}')


if __name__ == '__main__':
    app.run()
