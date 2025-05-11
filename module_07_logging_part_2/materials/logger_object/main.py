import logging
import flask

from http_utils import get_ip_address
from subprocess_utils import get_kernel_version

root_logger = logging.getLogger('root')
root_logger.setLevel('INFO')
main_logger = logging.getLogger('main')
main_logger.setLevel("INFO")
utils_logger = logging.getLogger('utils')
utils_logger.setLevel("DEBUG")


app = flask.Flask(__name__)


@app.route('/get_system_info')
def get_system_info():
    main_logger.info('Start main working')
    ip = get_ip_address()
    kernel = get_kernel_version()
    return "<p>{}</p><p>{}</p>".format(ip, kernel)


if __name__ == '__main__':
    print(root_logger, main_logger, utils_logger)
    app.run(debug=True)
