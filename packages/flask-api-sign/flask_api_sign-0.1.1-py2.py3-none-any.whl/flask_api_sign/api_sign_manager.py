# -*- coding: utf-8 -*-
# @author: juforg
# @email: juforg@sina.com
# @date: 2020/04/06
#      SJ编程规范
# 命名：
#    1. 见名思意，变量的名字必须准确反映它的含义和内容
#    2. 遵循当前语言的变量命名规则
#    3. 不要对不同使用目的的变量使用同一个变量名
#    4. 同个项目不要使用不同名称表述同个东西
#    5. 函数/方法 使用动词+名词组合，其它使用名词组合
# 设计原则：
#    1. KISS原则： Keep it simple and stupid !
#    2. SOLID原则： S: 单一职责 O: 开闭原则 L: 迪米特法则 I: 接口隔离原则 D: 依赖倒置原则
#


from flask import jsonify
from flask_api_sign.config import config
from flask_api_sign.exceptions import SignException, RequestExpiredError, NotConfigedAppIdsError, InvalidAppIdsTypeError, NotAllowedAppIdError, UnknowAppIdError


class ApiSignManager(object):
    def __init__(self, app=None):
        """
        Create the ApiSignManager instance. You can either pass a flask application
        in directly here to register this extension with the flask app, or
        call init_app after creating this object (in a factory pattern).

        :param app: A flask application
        """
        # Register the default error handler callback methods. These can be
        # overridden with the appropriate loader decorators
        # Register this extension with the flask app now (if it is provided)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Register this extension with the flask app.

        :param app: A flask application
        """
        # Save this so we can use it later in the extension
        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}
        app.extensions['flask-api-sign'] = self

        # Set all the default configurations for this extension
        self._set_default_configuration_options(app)
        self._set_error_handler_callbacks(app)

    @staticmethod
    def _set_error_handler_callbacks(app):
        """
        Sets the error handler callbacks used by this extension
        """

        @app.errorhandler(RequestExpiredError)
        def handle_error(e):
            return jsonify({config.error_msg_key: f'request timestamp expired：{e.args}'}), 408

        @app.errorhandler(SignException)
        def handle_error(e):
            return jsonify({config.error_msg_key: f'verification failed :{e.args}'}), 401

    @staticmethod
    def _set_default_configuration_options(app):
        """
        Sets the default configuration options used by this extension
        """
        # Where to look for the SIGN param.
        app.config.setdefault('SIGN_LOCATION', 'query_string')

        app.config.setdefault('SIGN_TIMESTAMP_NAME', 'timestamp')
        app.config.setdefault('SIGN_APP_ID_NAME', 'x-app-id')
        app.config.setdefault('SIGN_SIGNATURE_NAME', 'x-sign')
        app.config.setdefault('SIGN_REQUEST_ID_NAME', 'x-request-id')
        app.config.setdefault('SIGN_ACCESS_TOKEN_NAME', 'x-access-token')
        app.config.setdefault('SIGN_APP_SECRET_NAME', 'app-secret')

        # How long an a sign is valid.
        app.config.setdefault('SIGN_TIMESTAMP_EXPIRATION', 30)

        # What algorithm to use to sign . RSA SHA md5
        app.config.setdefault('SIGN_ALGORITHM', 'HS256')

        # Options for blacklisting/revoking tokens
        app.config.setdefault('SIGN_BLACKLIST_ENABLED', False)

        app.config.setdefault('SIGN_REQUIRE_SIGN', True)
        app.config.setdefault('SIGN_REQUIRE_TOKEN', False)

        app.config.setdefault('SIGN_ERROR_MSG_KEY', 'msg')

    @staticmethod
    def get_and_check_app_secret(app_id):
        """
        根据 app_id获取对应的 secret
        :param app_id:
        :return:
        """
        if not config.cust_check_app_id_func:
            if not config.app_ids:
                raise NotConfigedAppIdsError("appid list not configed")
            if not isinstance(config.app_ids, dict):
                raise InvalidAppIdsTypeError("appid list not a dict")
            app_secret = config.app_ids.get(app_id)
            if not app_secret:
                raise UnknowAppIdError(f"unknow app_id:{app_id}")
            else:
                return app_secret
        else:
            return config.cust_check_app_id_func(app_id)


class ApiSign(object):
    app_id = None
    request_id = None
    signature = None
    timestamp = None
    other_params = dict()

    def __init__(self, app_id=None, request_id=None, signature=None, timestamp=None, other_params=None):
        self.app_id = app_id
        self.request_id = request_id
        self.signature = signature
        self.timestamp = timestamp
        self.other_params = other_params

    def dict(self):
        d = {config.app_id: self.app_id,
             config.request_id: self.request_id,
             # config.data_key: self.other_params,
             config.timestamp: self.timestamp,
             }
        if self.other_params:
            d[config.data_key] = self.other_params
        return d
