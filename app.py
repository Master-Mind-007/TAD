#!/usr/bin/env python3
import asyncio

from functools import wraps
from sys import exit, setrecursionlimit
from re import search
from glob import glob
from time import sleep, perf_counter
from shutil import copy
from threading import Thread
from dotenv import load_dotenv
from traceback import print_exc
from importlib import import_module
from asyncio import sleep as asleep
from random import randint as randomise
from datetime import datetime, timedelta
from signal import signal, SIGINT, SIGTERM
from os import path, rename, remove, environ
from verboselogs import VerboseLogger, VERBOSE
from coloredlogs import install as Cloginstall
from phonenumbers import parse as pparse, format_number, PhoneNumberFormat
from logging import DEBUG

from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, jsonify

from pyrogram import Client
from pyrogram.errors import FloodWait, BadRequest, SessionPasswordNeeded, RPCError

start = perf_counter()

#Initialize Logger
logger = VerboseLogger('my_logger')
Cloginstall(level=VERBOSE, fmt='[%(asctime)s] | %(levelname)-8s | %(message)s')
load_dotenv('config.env', override=True)

#Initialize Flask
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///airdropper.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = ''

#Initialize Database
db = SQLAlchemy(app)

#Initialize Sessions
sessions = {}
config_classes = {}

# Initialize Environment Variables
OWNER_ID = environ.get('OWNER_ID', '')
TELEGRAM_API = environ.get('TELEGRAM_API', '')
TELEGRAM_HASH = environ.get('TELEGRAM_HASH', '')


### Initialize Database
# Table Accounts
class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_premium = db.Column(db.Boolean, nullable=True, default=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    username = db.Column(db.String, nullable=True)
    dc_id = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=False)
    status  = db.Column(db.String, nullable=True)
    last_sync = db.Column(db.DateTime, default=datetime.utcnow)
    running = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"{self.id} | {self.is_premium} | {self.first_name} | {self.username} | {self.dc_id} | {self.status} | {self.running}"

# Table Configurations
class Configurations(db.Model):
    config_name = db.Column(db.String(20), primary_key=True, nullable=False)
    status = db.Column(db.Boolean, nullable=True)
    runs = db.Column(db.Integer, nullable=True)
    success = db.Column(db.Integer, nullable=True)
    fails = db.Column(db.Integer, nullable=True)

    def __repr__(self) -> str:
        return f"{self.config_name} | {self.status} | {self.runs} | {self.success} | {self.fails}"

# Table Statistics
class Statistics(db.Model):
    label = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.String(20), nullable=True)
    change = db.Column(db.String(20), nullable=True)
    last_hour = db.Column(db.String(20), nullable=True)
    last_day = db.Column(db.Integer, nullable=True)
    last_week = db.Column(db.Integer, nullable=True)
    last_hour_change = db.Column(db.Integer, nullable=True)
    last_day_change = db.Column(db.Integer, nullable=True)
    last_week_change = db.Column(db.Integer, nullable=True)

    def __repr__(self) -> str:
        return f"{self.users} - {self.success}"



def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper


# Functions
def now():
    return datetime.now()


@memoize
def sync_session():
    @memoize
    def fetch_configs() -> list[str]:
        configs_path = glob('configs/*.py')
        configs_modules = [path.splitext(path.basename(file))[0] for file in configs_path]

        for config_name in configs_modules:
            try:
                module = import_module(f'configs.{config_name}')
                config_classes[config_name] = {}
                config_classes[config_name]["class"] = getattr(module, config_name)
                config_classes[config_name]["balanceModule"] = getattr(module, "balance")
                config_classes[config_name]["dbModule"] = getattr(module, "generate_db")
                config_classes[config_name]["runs"] = 0
                config_classes[config_name]["fails"] = 0
                config_classes[config_name]["success"] = 0
                config_classes[config_name]["totalBalance"] = 0
                
                db_func = config_classes[config_name]["dbModule"]
                db_func()

                logger.success(f"Imported Config: {config_name}")
            except Exception as e:
                logger.error(f"Failed to Import Config: {config_name}")
                logger.error(e)
        
        return len(config_classes)
    
    @memoize
    def fetch_sessions() -> list[str]:
        session_names = glob('sessions/*.session')
        session_names = [path.splitext(path.basename(file))[0] for file in session_names]
        return session_names
    
    fetch_configs()
    
    def db_update_run():
        with app.app_context():
            all_accounts = Accounts.query.all()
            for account in all_accounts:
                account.running = False
                db.session.commit()

    db_update_run()

    for session_name in fetch_sessions():
        try:
            client = Client(
                name=session_name, 
                api_id=TELEGRAM_API, 
                api_hash=TELEGRAM_HASH, 
                app_version="plus messenger 10.14.5.0", 
                device_model="Samsung Galaxy A31",
                system_version = "9 P (28)",
                max_concurrent_transmissions = 10,
                sleep_threshold = 120,
                takeout = True,
                no_updates = True,
                workers = 32,
                workdir = "sessions"
            )
            runner = TelegramClientRunner(client, session_name)
            runner.start(runner)
        except Exception as e:
            logger.error(f"Failed to connect session: {session_name}")
            logger.error(f"{e}")


def signal_handler(sig, frame):
    def stop_all_event_loops():
        event_loops = []
        for session, session_items in sessions.items():
            for config_name in session_items["instances"]:
                task = session_items["instances"][config_name]["instance_task"]
                session_items["instances"][config_name]["instance"].stop(task)
            loop = session_items["loop"]
            for task in asyncio.all_tasks(loop=loop):
                task.cancel()
            loop.call_soon_threadsafe(loop.stop)

    stop_all_event_loops()
    exit(0)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    shutdown()

class TelegramClientRunner:
    def __init__(self, client, session_name):
        self.client = client
        self.session_name = session_name
        self.loop = asyncio.new_event_loop()
        self.me = None

    async def run_client(self, runner):
        try:
            await self.client.connect()
            sessions[self.session_name] = {}
            sessions[self.session_name]["client"] = self.client
            sessions[self.session_name]["runner"] = runner
            sessions[self.session_name]["loop"] = self.loop
            sessions[self.session_name]["instances"] = {}
            return True
        except FloodWait as e:
            logger.notice(f"FloodWait | Sleeping for {e.value}s")
            await asleep(e.value)
        except (RPCError, BadRequest) as e:
            logger.critical(e)
            return False
        except Exception as e:
            logger.error(f"Error running client: {e}")
            return False

    async def client_sync_db(self):
        try:
            me = await self.client.get_me()
            self.me = me
            if me.id not in sessions[self.session_name]:
                sessions[self.session_name]["id"] = me.id
            
            with app.app_context():
                prev_data = db.session.get(Accounts, me.id)
                pnumber = pparse(f"+{me.phone_number}", None)
                if prev_data:
                    prev_data.is_premium = True if me.is_premium == 1 else False
                    prev_data.first_name = me.first_name
                    prev_data.last_name = me.last_name
                    prev_data.username = me.username
                    prev_data.dc_id = 'Unknown' if me.dc_id is None else me.dc_id
                    prev_data.phone_number = format_number(pnumber, PhoneNumberFormat.INTERNATIONAL)
                    prev_data.status = me.status.name
                    prev_data.last_sync = now()
                    prev_data.running = True
                else:
                    data = Accounts(
                        id=me.id,
                        is_premium= True if me.is_premium == 1 else False,
                        first_name=me.first_name,
                        last_name=me.last_name,
                        username=me.username,
                        dc_id= 'Unknown' if me.dc_id == None else me.dc_id,
                        phone_number=format_number(pnumber, PhoneNumberFormat.INTERNATIONAL),
                        status=me.status.name,
                        last_sync=now(),
                        running = True,
                    )
                    db.session.add(data)
                db.session.commit()
                logger.success(f"Telegram ID {me.id} synced successfully")
        except FloodWait as e:
            logger.notice(f"FloodWait | Sleeping for {e.value}s")
            await asleep(e.value)
        except (RPCError, BadRequest) as e:
            logger.critical(e)
        except Exception as e:
            logger.error(f"Error Updating DB: {e}")
            
    async def send_message_sync(self, chat_id, message):
        try:
            await self.client.send_message(chat_id, message)
        except FloodWait as e:
            logger.notice(f"FloodWait | Sleeping for {e.value}s")
            await asleep(e.value)
        except (RPCError, BadRequest) as e:
            logger.critical(e)
        except Exception as e:
            logger.error(f"Error sending message: {e}")


    def send_message(self, chat_id, message):
        self.loop.create_task(self.send_message_sync(chat_id, message))

    def sync_db(self):
        task = self.loop.create_task(self.client_sync_db())
        while not task.done():
            sleep(2)
        return


    def start(self, runner):
        status = self.loop.run_until_complete(self.run_client(runner))
        if status:
            self.loop.run_until_complete(self.client_sync_db())
            pyro_thread = Thread(target=self.loop.run_forever)
            pyro_thread.start()


class TelegramLogin:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = None
        self.loop = asyncio.new_event_loop()
        self.session = {}
    
    def rpc_match(self, e):
        match = search(r'Telegram says: \[(\d+ [A-Z_]+)\] - ([^\(]+)', str(e))
        if match:
            error_code = match.group(1)
            error_desc = match.group(2)
            return True, error_code, error_desc
        else:
            return False, None, None
    
    async def modify_session(self, phone_number):
        try:
            client = self.session[phone_number]['client']
            session_name = f"temp/{self.session[phone_number]['user_sesssion_name']}"
            me = await client.get_me()
            name = f"{me.first_name}_{me.last_name}"
            if path.exists(f"{session_name}.session"):
                copy(f"{session_name}.session", f"sessions/{name}.session")
                await client.stop()
                remove(f"{session_name}.session")
                    
                client = Client(
                    name=session_name, 
                    api_id=TELEGRAM_API, 
                    api_hash=TELEGRAM_HASH, 
                    app_version="plus messenger 10.14.5.0", 
                    device_model="Samsung Galaxy A31",
                    system_version = "9 P (28)",
                    max_concurrent_transmissions = 10,
                    sleep_threshold = 120,
                    takeout = True,
                    no_updates = True,
                    workers = 32,
                    workdir = "sessions"
                )
                runner = TelegramClientRunner(client, session_name)
                sessions[session_name]["runner"] = runner
                runner.start()

            logger.notice(f"Telegram Login | Modify Session | Session Modified: {name}")
        
        except FloodWait as e:
            logger.notice(f"FloodWait | Sleeping for {e.value}s")
            await asleep(e.value)
        except (RPCError, BadRequest) as e:
            logger.critical(e)
        except Exception as e:
            logger.warning(f"Telegram Login | Modify Session | Error: {e}")


    async def request_code(self, phone_number):
        try:
            self.session[phone_number] = {}
            self.session[phone_number]['user_sesssion_name'] = f'user_{randomise(00, 9999999)}'
            self.client = Client(
                name=self.session[phone_number]['user_sesssion_name'], 
                api_id=TELEGRAM_API, 
                api_hash=TELEGRAM_HASH, 
                app_version="plus messenger 10.14.5.0", 
                device_model="Samsung Galaxy A31",
                system_version = "9 P (28)",
                max_concurrent_transmissions = 10,
                sleep_threshold = 120,
                takeout = True,
                no_updates = True,
                workers = 32,
                workdir = "temp")
            await self.client.connect()
            self.session[phone_number]['client'] = self.client
        
        except FloodWait as e:
            logger.notice(f"FloodWait | Sleeping for {e.value}s")
            await asleep(e.value)
        except (RPCError, BadRequest) as e:
            logger.critical(e)
        except Exception as e:
            logger.warning(f"Telegram Client Connect Error: {e}")

        try:
            sent_code = await self.client.send_code(phone_number)
            status = self.session[phone_number]['phone_code_hash'] = sent_code.phone_code_hash
            logger.notice(f"Telegram Login | Request Code | Code Sent: +{phone_number}")
            return True, None, None
        except FloodWait as e:
            logger.notice(f"FloodWait | Sleeping for {e.value}s")
            await asleep(e.value)
            return False, None, 'flood wait'
        except (RPCError, BadRequest) as e:
            match, error_code, error_desc = self.rpc_match(e)
            if match:
                logger.error(f"Telegram Login | Login User | RPC Error: {e}")
                return False, error_code, error_desc
            else:
                logger.error(f"Telegram Login | Login User | Bad Request: {e}")
                return False, None, None
        except Exception as e:
            logger.error(f"Telegram Login | Request Code | Exception Error: {e}")
            return False, None, None

    async def login_user(self, phone_number, otp):
        try:
            if phone_number not in self.session:
                return False, "403", "Invalid Request"
            client = self.session[phone_number]['client']
            await client.sign_in(phone_number=phone_number, phone_code_hash=self.session[phone_number]['phone_code_hash'], phone_code=otp)
            if await client.get_me():
                await self.modify_session(phone_number)
                logger.notice("Telegram Login | Login User | Logged in successfully!")
                return True, None, None
            else:
                logger.error("Telegram Login | Login User | Failed to log in")
                return False, None, None

        except FloodWait as e:
            logger.notice(f"FloodWait | Sleeping for {e.value}s")
            await asleep(e.value)
            return False, None, 'flood wait'
        except SessionPasswordNeeded:
            logger.error("Telegram Login | Login User | Cloud Password is required")
            return False, None, 'password_required'
        except (RPCError, BadRequest) as e:
            match, error_code, error_desc = self.rpc_match(e)
            if match:
                logger.error(f"Telegram Login | Login User | RPC Error: {e}")
                return False, error_code, error_desc
            else:
                logger.error(f"Telegram Login | Login User | Bad Request: {e}")
                return False, None, None
        except Exception as e:
            logger.error(f"Telegram Login | Login User | Exception Error: {e}")
            return False, None, None

    async def login_user_password(self, phone_number, cloud_password):
        try:
            if phone_number not in self.session:
                return False, "403", "Invalid Request"
            if cloud_password:
                client = self.session[phone_number]['client']
                await client.check_password(cloud_password)
                if await client.get_me():
                    sleep(10)
                    await self.modify_session(phone_number)
                    logger.notice(f"Telegram Login | Login Password | Logged in successfully")
                    return True, None, None
                else:
                    logger.error("Telegram Login | Login Password | Failed to login")
                    return False, None, None
            else:
                logger.error("Cloud password is required but not provided.")
                return False, None, None
        except FloodWait as e:
            logger.notice(f"FloodWait | Sleeping for {e.value}s")
            await asleep(e.value)
            return False, None, 'flood wait'
        except (RPCError, BadRequest) as e:
            match, error_code, error_desc = self.rpc_match(e)
            if match:
                logger.error(f"Telegram Login | Login User | RPC Error: {e}")
                return False, error_code, error_desc
            else:
                logger.error(f"Telegram Login | Login User | Bad Request: {e}")
                return False, None, None
        except Exception as e:
            logger.error(f"Telegram Login | Login Password | Exception Error: {e}")
            return False, None, None


    def request_otp(self, phone_number):
        return self.loop.run_until_complete(self.request_code(phone_number))

    def login(self, phone_number, otp):
        return self.loop.run_until_complete(self.login_user(phone_number, otp))

    def login_password(self, phone_number, cloud_password):
        return self.loop.run_until_complete(self.login_user_password(phone_number, cloud_password))



### Initialize Flask
@app.template_filter('current_datetime')
def current_datetime():
    return datetime.now()


@app.route('/')
def index():
    change = 0
    last_hour = []
    last_week = []
    last_day = []
    last_hour_change = 0
    last_day_change = 0
    last_week_change = 0
    
    def accounts():
        allentry = Accounts.query.all()
        for entry in allentry:
            time_diff = now() - entry.last_sync
            if time_diff <= timedelta(hours=1):
                last_hour.append(entry)
            elif time_diff <= timedelta(days=1):
                last_day.append(entry)
            elif time_diff <= timedelta(weeks=1):
                last_week.append(entry)
        return {"label": "Accounts",
                "total": len(allentry),
                "change": change,
                "last_hour": len(last_hour), 
                "last_day": len(last_day), 
                "last_week": len(last_week), 
                "last_hour_change": last_hour_change, 
                "last_day_change": last_day_change, 
                "last_week_change": last_week_change}
    
    def airdrop_config():
        configs = []
        return {"label": "Airdrop Config",
                "total": len(configs),
                "change": change,
                "last_hour": len(last_hour),
                "last_day": len(last_day),
                "last_week": len(last_week),
                "last_hour_change": last_hour_change,
                "last_day_change": last_day_change,
                "last_week_change": last_week_change}
    
    def users():
        users = []
        return {"label": "Users",
                "total": len(users),
                "change": change,
                "last_hour": len(last_hour),
                "last_day": len(last_day),
                "last_week": len(last_week),
                "last_hour_change": last_hour_change,
                "last_day_change": last_day_change,
                "last_week_change": last_week_change}
    
    stats_data =  [accounts(), airdrop_config(), users()]
    return render_template('index.html', stats_data=stats_data)


@app.route('/accounts')
async def accounts():
    allaccounts = Accounts.query.all()
    return render_template('accounts.html', accounts=allaccounts, current_time=now())

@app.route('/raw/accounts', methods=['GET'])
def raw_accounts():
    allaccounts = Accounts.query.all()
    return render_template('accounts_table.html', accounts=allaccounts, current_time=now())

@app.route('/raw/refresh', methods=['GET'])
def refresh():
    global sessions
    for session, session_items in sessions.items():
        for config_name in session_items["instances"]:
            task = session_items["instances"][config_name]["instance_task"]
            session_items["instances"][config_name]["instance"].stop(task)
        loop = session_items["loop"]
        for task in asyncio.all_tasks(loop=loop):
            task.cancel()
        loop.call_soon_threadsafe(loop.stop)
    sessions = {}
    sync_session()
    allaccounts = Accounts.query.all()
    return render_template('accounts_table.html', accounts=allaccounts, current_time=now())


@app.route('/statistics')
async def statistics():
    return render_template('statistics.html')


@app.route('/configs')
async def configs():
    for config_name, config in config_classes.items():
        bal_func = config_classes[config_name]["balanceModule"]
        config_classes[config_name]["totalBalance"] = bal_func()
        config_classes[config_name]["runs"]  = 0
        config_classes[config_name]["fails"]  = 0
        config_classes[config_name]["success"]  = 0

    for session in sessions:
        try:
            for config_name, config in sessions[session]["instances"].items():
                stats = config["instance"].status()
                config_classes[config_name]["runs"] += stats["runs"]
                config_classes[config_name]["fails"] += stats["fails"]
                config_classes[config_name]["success"] += stats["success"]
            
        except Exception as e:
            logger.critical(print_exc())
            logger.critical(f"Configs Route Exception: {e}")

    return render_template('conf-2.html', configs=config_classes)


@app.route('/settings')
async def settings():
    return render_template('settings.html', configs=config_classes)

@app.route('/api/v1/login/phone', methods=['POST'])
def login_phone():
    data = request.json
    phone_number = data.get('phone_number')
    response = {'message': 'None', 'error': {"status": True}, 'status_code': 400}

    if not phone_number:
        response['message'] = 'Phone number is required'
    else:
        status, error_code, error_desc = telegram_login.request_otp(phone_number)
        if status:
            response['message'] = 'Code sent successfully'
            response['error']['status'] = False
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
    response = {'message': 'None', 'error': {"status": True}, 'status_code': 400}
    
    if not otp:
        response['message'] = 'OTP is required'
    elif not phone_number:
        response['message'] = 'Phone number is required'
    else:
        status, error_code, error_desc = telegram_login.login(phone_number, otp)
        if status:
            response['message'] = 'Logged in successfully'
            response['error']['status'] = False
            response['status_code'] = 200
        elif error_desc == 'password_required':
            response['message'] = 'Cloud password required'
            response['error']['status'] = False
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
    response = {'message': 'None', 'error': {"status": True}, 'status_code': 400}

    if not cloud_password:
        response['message'] = 'Cloud password is required'
    elif not phone_number:
        response['message'] = 'Phone number is required'
    else:
        status, error_code, error_desc = telegram_login.login_password(phone_number, cloud_password)
        if status:
            response['message'] = 'Logged in successfully'
            response['error']['status'] = False
            response['status_code'] = 200
        else:
            response['message'] = 'Failed to log in'
            if error_code:  
                response['error']['code'] = error_code
            if error_desc:
                response['error']['desc'] = error_desc
            response['status_code'] = 400

    return jsonify(response), response['status_code']


@app.route('/api/v1/account/sync', methods=['POST'])
async def loginSync():
    response =  {'message': 'None', 'error': {"status": True}, 'status_code': 400}
    if request.method=='POST':
        userid = request.json.get('userid')
        for session in sessions:
            if int(userid) == sessions[session]["id"]:
                client_session = sessions[session]["runner"]
                client_session.sync_db()
                response['message'] = 'Synced successfully'
                response['error']['status'] = False
                response['status_code'] = 200
                return jsonify(response), response['status_code']
        response['message'] = 'item not found'
        response['status_code'] = 404
    else:
        response['message'] = 'method not allowed'
        response['status_code'] = 405
    return jsonify(response), response['status_code']


@app.route('/api/v1/account/delete', methods=['POST'])
def accountDelete():
    response =  {'message': 'None', 'error': {"status": True}, 'status_code': 400}
    if request.method=='POST':
        userid = request.json.get('userid')
        entry = db.session.get(Accounts, userid)
        if entry:
            db.session.delete(entry)
            db.session.commit()
            logger.success(f"UserId: {userid} | Item Deleted Successfully")
            response['message'] = 'item deleted successfully'
            response['error']['status'] = False
            response['status_code'] = 200
        else:
            response['message'] = 'item not found'
            response['status_code'] = 404
    else:
        response['message'] = 'method not allowed'
    return jsonify(response), response['status_code']


# Function to create a route for each config class
@memoize
def create_config_routes(config_name, config_class):
    @memoize
    async def run_config():
        for session in sessions:
            try:
                if config_name not in sessions[session]["instances"]:
                    instance = config_class(sessions[session]["client"], sessions[session]["loop"])
                    sessions[session]["instances"][config_name] = {"instance": instance, "instance_task": instance.start()}
                    logger.success(f"Started {config_name} for session {session} successfully")
                else:
                    return "Already Running!"
            except Exception as e:
                logger.error(f"Failed to start {config_name} for session {session}: {e}")

    async def config_route_start():
        asyncio.create_task(run_config())
        return f"{config_name} started for all sessions"
    
    config_route_start.__name__ = f"config_route_start{config_name}"
    app.route(f'/config/{config_name}/start', methods=['GET'])(config_route_start)
    logger.success(f"Created Route for {config_name}")

    @memoize
    async def stop_config():
        for session in sessions:
            try:
                if config_name in sessions[session]["instances"]:
                    task = sessions[session]["instances"][config_name]["instance_task"]
                    sessions[session]["instances"][config_name]["instance"].stop(task)
                    logger.success(f"Stopped {config_name} for session {session} successfully")
                    sessions[session]["instances"].pop(config_name)
            except Exception as e:
                logger.error(f"Failed to stop {config_name} for session {session}: {e}")

    async def config_route_stop():
        asyncio.create_task(stop_config())
        return f"{config_name} stopped for all sessions"
    
    config_route_stop.__name__ = f"config_route_stop{config_name}"
    app.route(f'/config/{config_name}/stop', methods=['GET'])(config_route_stop)


if __name__ == '__main__':
    ### Initialize Exit Signals
    signal(SIGINT, signal_handler)
    signal(SIGTERM, signal_handler)

    # Initialize Database
    with app.app_context():
        if not path.exists("instance/airdropper.db"):
            db.create_all()
            logger.success("Created Database")

    ### Initialize Telegram Login
    telegram_login = TelegramLogin(TELEGRAM_API, TELEGRAM_HASH)

    # Initialize Sessions ans Configuration files
    sync_session()
    
    # Create routes for each config class
    for config_name, config_class in config_classes.items():
        create_config_routes(config_name, config_class["class"])

    end = perf_counter()

    print(f"Time Taken: {end - start}")
    # Initialize Flask
    app.run(debug=True, use_reloader=False)