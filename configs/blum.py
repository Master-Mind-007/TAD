#!/usr/bin/env python3

from app import app
from app import db
from sqlalchemy import inspect
from sqlalchemy.schema import CreateTable

from os import path
from glob import glob
from time import sleep, perf_counter
from urllib import parse
from pytz import timezone
from calendar import timegm
from base64 import b64decode
from datetime import datetime
from traceback import print_exc
from collections import defaultdict
from random import randint as randomise
from requests import get as rget, post as rpost
from json import loads as json, dumps as jsonify

from pyrogram.raw.types import Channel
from pyrogram.enums import ChatMemberStatus
from pyrogram.raw.base import WebViewResult
from pyrogram.raw.functions.messages import RequestWebView
from pyrogram.errors import ChatAdminRequired, UserNotParticipant

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, HardwareType, SoftwareType, SoftwareEngine

from coloredlogs import install
from verboselogs import VerboseLogger, VERBOSE

logger = VerboseLogger('my_logger')
install(level=VERBOSE, fmt='[%(asctime)s] | %(levelname)-8s | %(message)s')

softwares = [SoftwareName.FIREFOX.value]
ost = [OperatingSystem.IOS.value]
sengine = [SoftwareEngine.KHTML.value, SoftwareEngine.GECKO.value, SoftwareEngine.WEBKIT.value]
stype = [SoftwareType.WEB_BROWSER.value]
htype = [HardwareType.MOBILE__PHONE.value, HardwareType.MOBILE.value]

user_agent_rotator = UserAgent(software_names=softwares, operating_systems=ost, hardware_types=htype, software_types=stype, software_engines=sengine, limit=10000)

config_name = "blum"
create_db = True
clear_db = True
scheduler = {"time":  12 * 60 * 60}


class BLUM(db.Model):
	userid = db.Column(db.Integer, primary_key=True, nullable=False)
	balance = db.Column(db.Integer, nullable=False)

	def __repr__(self) -> str:
		return f"{self.userid} | {self.balance}"
	
class tweak_db:
	def __init__(self) -> None:
		pass
	
	def create_db(self):
		print("creating db")
		with app.app_context():
			if not inspect(db.engine).has_table(config_name):
				db.create_all()
				logger.notice(f"Created Table {config_name}")
			else:
				if clear_db:
					BLUM.__table__.drop(db.engine)
					logger.notice(f"Deleted existing Table {config_name}")
					db.create_all()

	def modify(self, userid, balance):
		with app.app_context():
			prev_data = db.session.get(BLUM, userid)
			if prev_data:
				prev_data.balance = balance
			else:
				data = BLUM(
					userid=int(userid),
					balance = int(balance)
				)
				db.session.add(data)
			db.session.commit()



class blum:
	def __init__(self, client, loop):
		self.client = client
		self.blum = 0
		self.proxy = self.prox()
		self.loop = loop
		self.referral_code = ""
		self.UA = user_agent_rotator.get_random_user_agent()
		self.stats = {"status": True, "runs": 0, "success": 0, "fails": 0}
		self.database = tweak_db()



	def ts(self):
		return round((datetime.now(pytz.timezone('UTC'))).timestamp()) - 1


	def prox(self):
		while error := True:
			proxy = "rp.proxyscrape.com:6060"
			password = "we3ipqif4m3jt7r"
			username = f"naert2grs9y9plq-country-us-session-osdiufoi{randomise(100, 10000)}-lifetime-120"
			proxy_auth = "{}:{}@{}".format(username, password, proxy)
			proxy = {"http":"http://{}".format(proxy_auth), "https":"http://{}".format(proxy_auth)}
			try:
				response = rget("https://api.hamsterkombatgame.io/ip", proxies=proxy)
				if "country_code" in response.text:
					error = False
					logger.notice(f"Established Proxy Connection: {json(response.text)['ip']}")
					return proxy
			except KeyboardInterrupt:
				break
			except Exception as e:
				error = True
				logger.warning(f"Bad Proxy!\n{e}")
				sleep(1)
				continue
		return 


	def Request(self, url, headers=None, json=None):
		while error := True:
			if self.stats["status"]:
				try:
					if json is None:
						response = rget(url, headers=headers, proxies=self.proxy)
					else:
						response = rpost(url, headers=headers, json=json, proxies=self.proxy)
					
					if response.status_code < 500:
						error = False
						return response
					else:
						sleep(2)
						pass
				except Exception as e:
					error = True
					logger.critical(f"Error in Requesting: {e}")
					sleep(1)

	def accountLog(self, auth):
		body = {"query": auth}
		print(body)
		headers = {
		'Host': 'gateway.blum.codes',
		'Content-Length': str(len(body)),
		'Sec-Ch-Ua': '"Chromium";v="113", "Not-A.Brand";v="24"',
		'Accept': 'application/json, text/plain, */*',
		'Content-Type': 'application/json',
		'Sec-Ch-Ua-Mobile': '?0',
		'User-Agent': self.UA,
		'Sec-Ch-Ua-Platform': '"Linux"',
		'Origin': 'https://telegram.blum.codes',
		'Sec-Fetch-Site': 'same-site',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Dest': 'empty',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'en-US,en;q=0.9'}

		response = self.Request("https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", headers=headers, json=body)
		print(response.text)
		return json(response.text)

	def accountRefresh(self):
		body = {"refresh": token}
		headers = {
		'Host': 'gateway.blum.codes',
		'Content-Length': str(len(body)),
		'Sec-Ch-Ua': '"Chromium";v="113", "Not-A.Brand";v="24"',
		'Accept': 'application/json, text/plain, */*',
		'Content-Type': 'application/json',
		'Sec-Ch-Ua-Mobile': '?0',
		'User-Agent': self.UA,
		'Sec-Ch-Ua-Platform': '"Linux"',
		'Origin': 'https://telegram.blum.codes',
		'Sec-Fetch-Site': 'same-site',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Dest': 'empty',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'en-US,en;q=0.9'}

		response = self.Request("https://gateway.blum.codes/v1/auth/refresh", headers=headers, json=body)
		return json(response.text)

	def accountBalance(self):
		headers = {
		"Host": 'game-domain.blum.codes',
		"User-Agent": self.UA,
		"Accept": 'application/json, text/plain, */*',
		"Accept-Language": 'en-US,en;q=0.5',
		"Accept-Encoding": 'gzip, deflate',
		"Authorization": f'Bearer {self.token}',
		"Origin": 'https://telegram.blum.codes',
		"Dnt": '1',
		"Sec-Fetch-Dest": 'empty',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Site": 'same-site',
		"Te": 'trailers'}

		response = self.Request("https://game-domain.blum.codes/api/v1/user/balance", headers=headers)
		return json(response.text)


	def farm(self, state):
		headers = {
		"Host": 'game-domain.blum.codes',
		"User-Agent": self.UA,
		"Accept-Language": 'en-US,en;q=0.5',
		"Accept-Encoding": 'gzip, deflate',
		"Authorization": f'Bearer {self.token}',
		"Origin": 'https://telegram.blum.codes',
		"Dnt": '1',
		"Sec-Fetch-Dest": 'empty',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Site": 'same-site',
		"Content-Length": '0',
		"Te": 'trailers'}

		response = self.Request(f"https://game-domain.blum.codes/api/v1/farming/{state}", headers=headers, json="")
		return json(response.text)


	def availableTasks(self):
		headers = {
		"Host": 'game-domain.blum.codes',
		"User-Agent": self.UA,
		"Accept": 'application/json, text/plain, */*',
		"Accept-Language": 'en-US,en;q=0.5',
		"Accept-Encoding": 'gzip, deflate',
		"Authorization": f'Bearer {self.token}',
		"Origin": 'https://telegram.blum.codes',
		"Dnt": '1',
		"Sec-Fetch-Dest": 'empty',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Site": 'same-site',
		"Te": 'trailers'}

		response = self.Request("https://game-domain.blum.codes/api/v1/tasks", headers=headers)
		return json(response.text)


	def performTasks(self, tid, state):
		headers = {
		"Host": 'game-domain.blum.codes',
		"User-Agent": self.UA,
		"Accept-Language": 'en-US,en;q=0.5',
		"Accept-Encoding": 'gzip, deflate',
		"Authorization": f'Bearer {self.token}',
		"Origin": 'https://telegram.blum.codes',
		"Dnt": '1',
		"Sec-Fetch-Dest": 'empty',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Site": 'same-site',
		"Content-Length": '0',
		"Te": 'trailers'}

		response = self.Request(f"https://game-domain.blum.codes/api/v1/tasks/{tid}/{state}", headers=headers, json="")
		return json(response.text)


	def dailyLogin(self):
		headers = {
		"Host": 'game-domain.blum.codes',
		"User-Agent": self.UA,
		"Accept": 'application/json, text/plain, */*',
		"Accept-Language": 'en-US,en;q=0.5',
		"Accept-Encoding": 'gzip, deflate',
		"Authorization": f'Bearer {self.token}',
		"Origin": 'https://telegram.blum.codes',
		"Dnt": '1',
		"Sec-Fetch-Dest": 'empty',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Site": 'same-site',
		"Te": 'trailers'}

		response = self.Request(f"https://game-domain.blum.codes/api/v1/daily-reward?offset=-330", headers=headers)
		if "message" not in json(response.text):
			response = self.Request(f"https://game-domain.blum.codes/api/v1/daily-reward?offset=-330", headers=headers, json="")
			logger.success("Daily Login Successfull!")
		return response.text

	def fetchTribe(self):
		headers = {
		"Host": 'game-domain.blum.codes',
		"User-Agent": self.UA,
		"Accept": 'application/json, text/plain, */*',
		"Accept-Language": 'en-US,en;q=0.5',
		"Accept-Encoding": 'gzip, deflate',
		"Authorization": f'Bearer {self.token}',
		"Origin": 'https://telegram.blum.codes',
		"Dnt": '1',
		"Sec-Fetch-Dest": 'empty',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Site": 'same-site',
		"Te": 'trailers'}

		response = self.Request("https://tribe-domain.blum.codes/api/v1/tribe/my", headers=headers)
		return json(response.text)


	def joinTribe(self):
		headers = {
		"Host": 'game-domain.blum.codes',
		"User-Agent": self.UA,
		"Accept-Language": 'en-US,en;q=0.5',
		"Accept-Encoding": 'gzip, deflate',
		"Authorization": f'Bearer {self.token}',
		"Origin": 'https://telegram.blum.codes',
		"Dnt": '1',
		"Sec-Fetch-Dest": 'empty',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Site": 'same-site',
		"Content-Length": '0',
		"Te": 'trailers'}

		response = self.Request(f"https://tribe-domain.blum.codes/api/v1/tribe/0999c4b7-1bbd-4825-a7a0-afc1bfb3fff6/join", headers=headers, json="")
		return response.text


	def gameStart(self):
		headers = {
		"Host": 'game-domain.blum.codes',
		"User-Agent": self.UA,
		"Accept-Language": 'en-US,en;q=0.5',
		"Accept-Encoding": 'gzip, deflate',
		"Authorization": f'Bearer {self.token}',
		"Origin": 'https://telegram.blum.codes',
		"Dnt": '1',
		"Sec-Fetch-Dest": 'empty',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Site": 'same-site',
		"Content-Length": '0',
		"Te": 'trailers'}

		response = self.Request(f"https://game-domain.blum.codes/api/v1/game/play", headers=headers, json="")
		return json(response.text)


	def gameEnd(self, gid):
		body = {"gameId": gid,"points": randomise(140, 180)}
		headers = {
		"Host": 'game-domain.blum.codes',
		"User-Agent": self.UA,
		"Accept": 'application/json, text/plain, */*',
		"Accept-Language": 'en-US,en;q=0.5',
		"Accept-Encoding": 'gzip, deflate',
		"Content-Type": 'application/json',
		"Authorization": f'Bearer {self.token}',
		"Content-Length": str(len(body)),
		"Origin": 'https://telegram.blum.codes',
		"Dnt": '1',
		"Sec-Fetch-Dest": 'empty',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Site": 'same-site',
		"Te": 'trailers',}

		response = self.Request(f"https://game-domain.blum.codes/api/v1/game/claim", headers=headers, json=body)
		return response.text



	async def run(self):
		if self.stats["status"]:
			try:
				self.stats["runs"] += 1
				me = await self.client.get_me()
				bot_peer = await self.client.resolve_peer("blumcryptobot")

				if (await self.client.get_chat_history_count(bot_peer.user_id)) == 0:
					await self.client.send_message("blumcryptobot", "/start")

				web_view: WebViewResult = await self.client.invoke(RequestWebView(
					peer=bot_peer,
					bot=bot_peer,
					start_param=self.referral_code,
					platform="ios",
					url="https://telegram.blum.codes/",
					silent=True
				))
				
				auth = parse.parse_qs(parse.urlparse(web_view.url).fragment)["tgWebAppData"][0]
				account = self.accountLog(auth)
				if "token" in account:
					await self.initialize(account)
			except Exception as e:
				logger.warning(e)
				self.stats["fails"] += 1
				return None


	async def initialize(self, account):
		token = account["token"]["access"]
		refresh = account["token"]["refresh"]
		user_id = account["token"]["user"]["id"]["id"]
		username = account["token"]["user"]["username"]
		is_new = account["justCreated"]
		self.token = token

		ab = self.accountBalance()
		balance = float(ab["availableBalance"])
		passbal = ab["playPasses"]
		farming = ab["isFastFarmingEnabled"]

		logger.success(f"User ID: {user_id}")
		logger.success(f"Username: {username}")
		logger.success(f"Is New: {is_new}")
		logger.success(f"BLUM: {balance}")
		logger.success(f"Play Pass: {passbal}")
		logger.success(f"Fast Farming: {farming}")

		self.dailyLogin()
		print(ab)

		if "farming" not in ab:
			logger.notice("Starting Farming...")
			fs = self.farm("start")
			if "earningsRate" in fs:
				logger.success("Farming Started!")
		if "farming" in ab:
			if ab["farming"]["endTime"] << ts():
				fs = self.farm("claim")
				if "message" not in fs:
					logger.success("Farming Yield Collected!")
					fs = self.farm("claim")
					if "earningsRate" in fs:
						logger.success("Farming Started!")

		while passbal > 0:
			logger.notice("Starting Game...")
			gid = self.gameStart()
			if "gameId" in gid:
				passbal -= 1
				logger.success(f"Started Game | Available Pass: {passbal}")
				sleep(randomise(28, 30))
				gstatus = self.gameEnd(gid["gameId"])
				if gstatus == "OK":
					logger.success(f"Game Completed | Available Pass: {passbal}")

		if "id" not in self.fetchTribe():
			if self.joinTribe() == "OK":
				logger.notice("Joined DOGS Tribe!")

		tasks = self.availableTasks()
		for section in tasks:
			task = section["tasks"]
			for atask in task:
				try:
					tid = atask["id"]
					title = atask["title"]
					reward = float(atask["reward"])

					if atask["type"] == "SOCIAL_SUBSCRIPTION" or tid == "ee7f9854-7ad7-4d95-9e4a-0ffb4210b0fa":
						if atask["status"] == "STARTED" or (atask["status"] == "READY_FOR_CLAIM"):
							pft = self.performTasks(tid, "claim")
							if ("message" not in pft) and (pft["status"] == "FINISHED"):
								balance += reward
								logger.success(f"Completed Task: {title} | Reward: +{reward} | Balance: {balance}")
						
						if atask["status"] == "NOT_STARTED":
							pft = self.performTasks(tid, "start")
							if ("message" not in pft) and pft["status"] == "STARTED":
								logger.notice(f"Started Task: {title} | Reward: {reward}")
								sleep(3)
								pft = self.performTasks(tid, "claim")
								if ("message" not in pft) and ((pft["status"] == "FINISHED") or (pft["status"] == "READY_FOR_CLAIM")):
									balance += reward
									logger.success(f"Completed Task: {title} | Reward: +{reward} | Balance: {balance}")
					
				except Exception as e:
					logger.error(f"Exception Occured while completing task! | {e}")
					logger.critical(print_exc())
					
		self.blum = balance
		self.stats["success"] += 1
	
		return True

	async def start_task(self):
		while self.stats["status"]:
			start = perf_counter()
			logger.notice(f'Status: {self.stats["status"]} | Run: {self.stats["runs"]} | Success: {self.stats["success"]} | Fail: {self.stats["fails"]}')
			await self.run()
			logger.success(f"Task Finished | {scheduler['time']}s Sleep")
			end = perf_counter()
			logger.notice(f"Performance Time: {end-start} seconds")
			await asleep(scheduler["time"])

	def start(self):
		return self.loop.create_task(self.start_task())

	def stop(self, task):
		logger.notice(f'Status: {self.stats["status"]} | Run: {self.stats["runs"]} | Success: {self.stats["success"]} | Fail: {self.stats["fails"]}')
		task.cancel()
		self.stats["status"] = False
		logger.success(f"Task Stopped!")
		return True
	
	def status(self):
		return self.stats


def balance():
	with app.app_context():
		return sum([blum.balance for blum in BLUM.query.all()])

def generate_db():
	if create_db:
		print("on creation")
		database = tweak_db()
		database.create_db()
