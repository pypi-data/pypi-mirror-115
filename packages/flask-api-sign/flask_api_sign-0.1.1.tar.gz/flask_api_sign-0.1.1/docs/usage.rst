=====
Usage
=====

To use Flask Api Sign in a project::

    import flask_api_sign

------------------------------
Configuring flask-api-sign
------------------------------
**flask-api-sign** is configured through the standard Flask config API. These are the available
options (each is explained later in the documentation):

* **SIGN_LOCATION** : default **query_string**

* **SIGN_TIMESTAMP_EXPIRATION** : default **30**
* **SIGN_APP_IDS** : default **``{'testapp': 'testsecret'}``**

verification is managed through a ``ApiSignManager`` instance::

    from flask import Flask
    from flask_api_sign import ApiSignManager

    app = Flask(__name__)
    api_sign_mgr = ApiSignManager(app)

In this case all verification using the configuration values of the application that
was passed to the ``ApiSignManager`` class constructor.

Alternatively you can set up your ``ApiSignManager`` instance later at configuration time, using the
**init_app** method::

    from flask import Flask
    api_sign_mgr = ApiSignManager()
    app = Flask(__name__)
    api_sign_mgr.init_app(app)

In this case verification will use the configuration values from Flask's ``current_app``
context global. This is useful if you have multiple applications running in the same
process but with different configuration options.


::::::::::::::::::::::::::::
Flask Api Sign Verification
::::::::::::::::::::::::::::
To generate a serial number first create a ``ApiSignManager`` instance::

    from flask import Flask
    from flask_api_sign import ApiSignManager
    from flask_api_sign import verify_sign

    app = Flask(__name__)

    api_sign_mgr = ApiSignManager()
    api_sign_mgr.init_app(app)
    @app.route("/")
    @verify_sign
    def index():
        pass


.. code-block :: java
    public class ApiSignTest {
        private static final String MD5 = "MD5";
        private static final int MD5_LENGTH = 32;
        public static String md5(byte[] bytes) {
            String result = null;
            try {
                MessageDigest md = MessageDigest.getInstance(MD5);
                md.update(bytes);
                String dig_result = new BigInteger(1, md.digest()).toString(16);
                if (dig_result.length() < MD5_LENGTH) {
                    StringBuffer sb = new StringBuffer(MD5_LENGTH);
                    int lack = MD5_LENGTH - dig_result.length();
                    for (int i = 0; i < lack; i++) {
                        sb.append("0");
                    }
                    sb.append(dig_result);
                    result = sb.toString();
                }
            } catch (NoSuchAlgorithmException e) {
                e.printStackTrace();
            }
            return result;
        }
        public static void main(String[] args) throws UnsupportedEncodingException {
            String appId = "testapp";
            String xRequestId = "11111";
            String timestamp = "1627914994";
            String secret = "ssss";
            String xData = "{\n" +
                    "    \"version\": \"1.0.0.1\",\n" +
                    "    \"timestamp\": 1616497374,\n" +
                    "    \"agv_info\": [\n" +
                    "        {\n" +
                    "            \"agv_name\": \"A002\",\n" +
                    "            \"agv_type\": \"type1\",\n" +
                    "            \"agv_state\" : \"ISOLATION\",\n" +
                    "            \"cur_node\": \"NN1\",\n" +
                    "            \"cur_head\": \"f\",\n" +
                    "            \"cur_angle\": \"01\",\n" +
                    "            \"destn_node\": \"NN4\",\n" +
                    "            \"destn_head\": \"\",\n" +
                    "            \"destn_angle\": \"\",\n" +
                    "            \"is_need_routing\": \"y\",\n" +
                    "            \"task_path\": [],\n" +
                    "            \"task_path_passed\": []\n" +
                    "        }\n" +
                    "    ]\n" +
                    "}";
            StringBuffer sb = new StringBuffer();
            sb.append("timestamp=").append(timestamp).append("&");
            sb.append("x-app-id=").append(appId).append("&");
            sb.append("x-data=").append(Base64.getUrlEncoder().encodeToString(xData.getBytes("utf-8"))).append("&");
            sb.append("x-request-id=").append(xRequestId).append("&");
            sb.append(secret);
            String signStr = md5(sb.toString().getBytes());
            System.out.println(signStr);
        }
    }

you can write a java client with the demo to generate the x-sign.

.. code-block :: bash
    curl --location --request POST 'http://127.0.0.1:5003/api/v1/routing' \
    --header 'x-app-id: testapp' \
    --header 'x-request-id: 11111' \
    --header 'x-sign: 920a476ecc10141a1d51ad3cf94d8287' \
    --header 'timestamp: 1627914994' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "version": "1.0.0.1",
    "timestamp": 1616497374,
    "agv_info": [
    {
    "agv_name": "A002",
    "agv_type": "type1",
    "agv_state" : "ISOLATION",
    "cur_node": "NN1",
    "cur_head": "f",
    "cur_angle": "01",
    "destn_node": "NN4",
    "destn_head": "",
    "destn_angle": "",
    "is_need_routing": "y",
    "task_path": [],
    "task_path_passed": []
    }
    ]
    }'

NOTE: Remember to set the secret key of the application, and ensure that no
one else is able to view it. The request are signed with the secret key, so
if someone gets that, they can create arbitrary request.
