import asyncio
from re import search
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, BadRequest, RPCError
from flask import Flask, request, jsonify, session
from random import randint as randomise

app = Flask(__name__)
app.secret_key = ""

TELEGRAM_API = 12220268
TELEGRAM_HASH = "8555236aba57fb960d73b6ca980226ae"

class TelegramLogin:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = None
        self.loop = asyncio.new_event_loop()
        self.session = {}

    async def request_code(self, phone_number):
        self.session[phone_number] = {}
        self.session[phone_number]['user_sesssion_name'] = f'user_{randomise(0000, 9999)}'
        self.client = Client(self.session[phone_number]['user_sesssion_name'], api_id=self.api_id, api_hash=self.api_hash)
        await self.client.connect()
        self.session[phone_number]['client'] = self.client
        try:
            sent_code = await self.client.send_code(phone_number)
            status = self.session[phone_number]['phone_code_hash'] = sent_code.phone_code_hash
            print(f"Telegram Login | Request Code | Code Sent: +{phone_number}")
            return True, None, None
        except (RPCError, BadRequest) as e:
            match = search(r'Telegram says: \[(\d+ [A-Z_]+)\] - ([^\(]+)', str(e))
            if match:
                error_code = match.group(1)
                error_desc = match.group(2)
                print(f"Telegram Login | Login User | RPC Error: {e}")
                return False, error_code, error_desc
            else:
                print(f"Telegram Login | Login User | Bad Request: {e}")
                return False, None, None
        except Exception as e:
            print(f"Telegram Login | Request Code | Exception Error: {e}")
            return False, None, None

    async def login_user(self, phone_number, otp):
        try:
            if phone_number not in self.session:
                return False, "403", "Invalid Request"
            client = self.session[phone_number]['client']
            await client.sign_in(phone_number=phone_number, phone_code_hash=self.session[phone_number]['phone_code_hash'], phone_code=otp)
            if client.get_me():
                print("Logged in successfully!")
                return True, None, None
            else:
                print("Telegram Login | Login User | Failed to log in")
                return False, None, None

        except SessionPasswordNeeded:
            print("Telegram Login | Login User | Cloud Password is required")
            return False, None, 'password_required'
        except (RPCError, BadRequest) as e:
            match = search(r'Telegram says: \[(\d+ [A-Z_]+)\] - ([^\(]+)', str(e))
            if match:
                error_code = match.group(1)
                error_desc = match.group(2)
                print(f"Telegram Login | Login User | RPC Error: {e}")
                return False, error_code, error_desc
            else:
                print(f"Telegram Login | Login User | Bad Request: {e}")
                return False, None, None
        except Exception as e:
            print(f"Telegram Login | Login User | Exception Error: {e}")
            return False, None, None

    async def login_user_password(self, phone_number, cloud_password):
        try:
            if phone_number not in self.session:
                return False, "403", "Invalid Request"
            if cloud_password:
                client = self.session[phone_number]['client']
                await client.check_password(cloud_password)
                if client.get_me():
                    print(f"Telegram Login | Login Password | successful")
                    return True, None, None
                else:
                    print("Telegram Login | Login Password | Failed to login")
                    return False, None, None
            else:
                print("Cloud password is required but not provided.")
                return False, None, None
        except (RPCError, BadRequest) as e:
            match = search(r'Telegram says: \[(\d+ [A-Z_]+)\] - ([^\(]+)', str(e))
            if match:
                error_code = match.group(1)
                error_desc = match.group(2)
                print(f"Telegram Login | Login User | RPC Error: {e}")
                return False, error_code, error_desc
            else:
                print(f"Telegram Login | Login User | Bad Request: {e}")
                return False, None, None
        except Exception as e:
            print(f"Telegram Login | Login Password | Exception Error: {e}")
            return False, None, None


    def request_otp(self, phone_number):
        return self.loop.run_until_complete(self.request_code(phone_number))

    def login(self, phone_number, otp):
        return self.loop.run_until_complete(self.login_user(phone_number, otp))

    def login_password(self, phone_number, otp, cloud_password=None):
        return self.loop.run_until_complete(self.login_user_password(phone_number, cloud_password))

telegram_login = TelegramLogin(TELEGRAM_API, TELEGRAM_HASH)


@app.route('/api/v1/login/phone', methods=['POST'])
def login_phone():
    data = request.json
    phone_number = data.get('phone_number')
    response = {'message': 'None', 'error': {"status": "true"}, 'status_code': 400}

    if not phone_number:
        response['message'] = 'Phone number is required'
    else:
        status, error_code, error_desc = telegram_login.request_otp(phone_number)
        if status:
            response['message'] = 'Code sent successfully'
            response['error']['status'] = 'false'
            response['status_code'] = 200
        else:
            response['message'] = f'Failed to send code'
            if error_code:  
                response['error']['code'] = error_code
            if error_desc:
                response['error']['desc'] = error_desc
            response['status_code'] = 400

    return jsonify(response), response['status_code']

@app.route('/api/v1/login/otp', methods=['POST'])
def login_otp():
    data = request.json
    otp = data.get('otp')
    phone_number = data.get('phone_number')
    response = {'message': 'None', 'error': {"status": "true"}, 'status_code': 400}
    
    if not otp:
        response['message'] = 'OTP is required'
    elif not phone_number:
        response['message'] = 'Phone number is required'
    else:
        status, error_code, error_desc = telegram_login.login(phone_number, otp)
        if status:
            response['message'] = 'Logged in successfully'
            response['error']['status'] = 'false'
            response['status_code'] = 200
        elif error_desc == 'password_required':
            response['message'] = 'Cloud password required'
            response['error']['status'] = 'false'
            response['status_code'] = 200
        else:
            response['message'] = 'Failed to log in'
            if error_code:  
                response['error']['code'] = error_code
            if error_desc:
                response['error']['desc'] = error_desc
            response['status_code'] = 400

    return jsonify(response), response['status_code']


@app.route('/api/v1/login/password', methods=['POST'])
def login_password():
    data = request.json
    phone_number = data.get('phone_number')
    cloud_password = data.get('cloud_password')
    response = {'message': 'None', 'error': {"status": "true"}, 'status_code': 400}

    if not cloud_password:
        response['message'] = 'Cloud password is required'
    elif not phone_number:
        response['message'] = 'Phone number is required'
    else:
        status, error_code, error_desc = telegram_login.login_password(phone_number, cloud_password)
        if status:
            response['message'] = 'Logged in successfully'
            response['error']['status'] = 'false'
            response['status_code'] = 200
        else:
            response['message'] = 'Failed to log in'
            if error_code:  
                response['error']['code'] = error_code
            if error_desc:
                response['error']['desc'] = error_desc
            response['status_code'] = 400

    return jsonify(response), response['status_code']

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)