#!/usr/bin/env python3

import requests

from urllib import parse
from pyrogram.raw.functions.messages import RequestWebView

from pyrogram.raw.base import WebViewResult
from json import loads as json
from asyncio import sleep as asleep
from base64 import b64decode
from random import randint as randomise
from traceback import print_exc

from coloredlogs import install
from verboselogs import VerboseLogger, VERBOSE

logger = VerboseLogger('my_logger')
install(level=VERBOSE, fmt='[%(asctime)s] | %(levelname)-6s | %(message)s')

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, HardwareType, SoftwareType, SoftwareEngine


softwares = [SoftwareName.FIREFOX.value]
ost = [OperatingSystem.IOS.value]
sengine = [SoftwareEngine.KHTML.value, SoftwareEngine.GECKO.value, SoftwareEngine.WEBKIT.value]
stype = [SoftwareType.WEB_BROWSER.value]
htype = [HardwareType.MOBILE__PHONE.value, HardwareType.MOBILE.value]

user_agent_rotator = UserAgent(software_names=softwares, operating_systems=ost, hardware_types=htype, software_types=stype, software_engines=sengine, limit=10000)


scheduler = {"time":  8 * 60 * 60}
major_web = "https://major.glados.app"


class major:
	def __init__(self, client, loop):
		print("Running into MAJOR")
		self.client = client
		self.balance = 0
		self.loop = loop
		self.referral_code = ""
		self.stats = {"status": True, "runs": 0, "success": 0, "fails": 0}

	def prox(self):
		error = True
		while error:
			proxy = "rp.proxyscrape.com:6060"
			password = "we3ipqif4m3jt7r"
			username = f"naert2grs9y9plq-country-us-session-osdisdfgsdfg{randomise(1000, 9000)}-lifetime-120"
			proxy_auth = "{}:{}@{}".format(username, password, proxy)
			proxy = {"http":"http://{}".format(proxy_auth), "https":"http://{}".format(proxy_auth)}
			try:
				response = requests.get("https://api.hamsterkombatgame.io/ip", proxies=proxy)
				if "country_code" in response.text:
					error = False
					logger.warning(f"Fetched Proxy: {json(response.text)['ip']}")
					return proxy
			except KeyboardInterrupt:
				break
			except:
				logger.warning("Bad Proxy!")
				error = True
				continue


	def Request(self, url, headers=None, json=None):
		error = True
		while error:
			try:
				if json is None:
					response = requests.get(url, headers=headers, proxies=self.proxy)
				else:
					response = requests.post(url, headers=headers, json=json, proxies=self.proxy)
				if response.status_code == 502:
					continue
				error = False
				return response
				break
			except Exception as e:
				logger.warning(f"Error in Requesting: {e}")
				error = True
				continue



	async def sessionAuth(self):
		try:
			peer = await self.client.resolve_peer("major")
			try:
				await self.client.join_chat("starsmajor")
				#if (await app.get_chat_history_count(peer.user_id)) == 0:
				#	await app.send_message("major", "/start")
			except Exception as e:
				logger.warning(e)
			web_view: WebViewResult = await self.client.invoke(RequestWebView(
				peer=peer,
				bot=peer,
				platform="android",
				url=major_web,
				start_param="1191266989",
				from_bot_menu=True
			))
				
			auth_url = web_view.url
			return parse.parse_qs(parse.urlparse(auth_url).fragment)["tgWebAppData"][0]
		except Exception as e:
			logger.warning(e)
			return None
	
	def accountAuth(self, auth):
		body = {"init_data": auth}
		head = {
		"Host": "major.glados.app",
		"User-Agent": self.UA,
		"Accept": "application/json, text/plain, */*",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Content-Type": "application/json",
		"Content-Length": str(len(body)),
		"Origin": "https://major.glados.app",
		"Referer": "https://major.glados.app/?tgWebAppStartParam=1191266989",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-origin",
		"Te": "trailers",}

		req = self.Request("https://major.glados.app/api/auth/tg/", headers=head, json=body)
		return json(req.text) if "access_token" in req.text else False


	def accountInfo(self):
		head = {
		"Host": "major.glados.app",
		"User-Agent": self.UA,
		"Accept": "application/json, text/plain, */*",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Authorization": f"Bearer {self.auth}",
		"Referer": "https://major.glados.app/",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-origin",
		"Te": "trailers",}

		req = self.Request(f"https://major.glados.app/api/users/{self.userid}/", headers=head)
		return json(req.text)


	def accountStreak(self):
		head = {
		"Host": "major.glados.app",
		"User-Agent": self.UA,
		"Accept": "application/json, text/plain, */*",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Authorization": f"Bearer {self.auth}",
		"Referer": "https://major.glados.app/",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-origin",
		"Te": "trailers",}

		req = self.Request("https://major.glados.app/api/user-visits/streak/", headers=head)
		logger.success(f"Streak Days: {json(req.text)['streak']}")
		return json(req.text)

	def accountVisits(self):
		try:
			head = {
			"Host": "major.glados.app",
			"User-Agent": self.UA,
			"Accept": "application/json, text/plain, */*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate",
			"Authorization": f"Bearer {self.auth}",
			"Referer": "https://major.glados.app/",
			"Origin": "https://major.glados.app",
			"Content-Lenth": "0",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"Te": "trailers",}

			req = self.Request("https://major.glados.app/api/user-visits/visit/", headers=head, json="")

			if json(req.text)["is_increased"] == True:
				logger.success("Login Streak Claimed!")
			return json(req.text)
		except Exception as e:
			logger.warning(e)

	def accountSpin(self):
		head = {
		"Host": "major.glados.app",
		"User-Agent": self.UA,
		"Accept": "application/json, text/plain, */*",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Authorization": f"Bearer {self.auth}",
		"Referer": "https://major.glados.app/",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-origin",
		"Te": "trailers",}

		req = self.Request("https://major.glados.app/api/roulette", headers=head, json="")
		if "rating_award" in req.text:
			logger.success(f"Spin Claimed: {json(req.text)['rating_award']}")
		return json(req.text)


	def tasks(self):
		head = {
		"User-Agent": self.UA,
		"Accept": "application/json, text/plain, */*",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Content-Type": "application/json",
		"Authorization": f"Bearer {self.auth}",
		"Referer": "https://major.glados.app/",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-origin",
		"Te": "trailers",}

		tasks = []

		reqA = self.Request("https://major.glados.app/api/tasks/?is_daily=false", headers=head)
		for task in json(reqA.text):
			tasks.append(task["id"])

		reqB = self.Request("https://major.glados.app/api/tasks/?is_daily=true", headers=head)
		for task in json(reqB.text):
			tasks.append(task["id"])

		return tasks

	def taskClaim(self, id):
		try:
			body = {"task_id": id}
			head = {
			"User-Agent": self.UA,
			"Accept": "application/json, text/plain, */*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate",
			"Content-Type": "application/json",
			"Authorization": f"Bearer {self.auth}",
			"Content-Length": str(len(body)),
			"Origin": "https://major.glados.app",
			"Referer": "https://major.glados.app/earn",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"Te": "trailers",}

			req = self.Request("https://major.glados.app/api/tasks/", headers=head, json=body)

			if "already completed" in req.text:
				logger.notice("Task is already completed")
				return(json(req.text))
			if "not available" in req.text:
				logger.notice("Task Unavailable")
				return(json(req.text))
			else:
				if json(req.text)["is_completed"] == True:
					logger.notice("Task Completed!")
				else:
					logger.success("Task not Completed!")
				return json(req.text)
		except Exception as e:
			logger.warning(e)
		

	async def run(self):
		try:
			print("started!")
			self.stats["runs"] += 1
			self.proxy = self.prox()
			self.UA = user_agent_rotator.get_random_user_agent()
			client_auth = await self.sessionAuth()
			auth = self.accountAuth(client_auth)
		
			if auth:
				self.userid = auth["user"]["id"]
				self.auth = auth["access_token"]
				if self.auth is not False:
					Info = self.accountInfo()
					for task_id in self.tasks():
						if task_id in ["8ace59a2-b89f-4051-b89e-94520440716e", "ff6556db-a5df-46ca-bbce-e4c8709e051b", "988006d6-be6a-4b3b-ac21-7992d5494bce", "08389d5b-29a9-489e-9d51-c8759c73a3f2", "573eb730-df1b-48fa-8921-a2ac6c7b41df", "52e30d38-37e3-455b-8bb4-503eaf600536"]:
							self.taskClaim(task_id)
					self.accountStreak()
					self.accountVisits()
					self.accountSpin()
					self.balance = Info["rating"]
					logger.success(f'{Info["username"]}:{self.balance}')
					self.stats["success"] += 1
					return
			self.stats["fails"] += 1
			return
		except Exception as e:
			logger.warning(e)
		
	async def start_task(self):
		try:
			while self.stats["status"]:
				print("running task")
				logger.notice(f'Status: {self.stats["status"]} | Run: {self.stats["runs"]} | Success: {self.stats["success"]} | Fail: {self.stats["fails"]}')
				await self.run()
				logger.success(f"Task Finished | {scheduler['time']}s Sleep")
				await asleep(scheduler["time"])
		except Exception as e:
			logger.warning(e)
			logger.warning(print_exc())
			return False

	def start(self):
		try:
			return self.loop.create_task(self.start_task())
		except Exception as e:
			logger.warning(e)
			logger.warning(print_exc())
			return False

	def stop(self, task):
		try:
			logger.notice(f'Status: {self.stats["status"]} | Run: {self.stats["runs"]} | Success: {self.stats["success"]} | Fail: {self.stats["fails"]}')
			task.cancel()
			self.stats["status"] = False
			logger.success(f"Task Stopped!")
			return True
		except Exception as e:
			logger.warning(e)
			logger.warning(print_exc())
			return False