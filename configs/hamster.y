#!/usr/bin/env python3

from os import path
from glob import glob
from time import sleep
from urllib import parse
from pytz import timezone
from datetime import datetime
from json import loads as json
from traceback import print_exc
from random import randint as randomise
from requests import get as rget, post as rpost

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, HardwareType, SoftwareType, SoftwareEngine

from pyrogram.enums import ChatMemberStatus
from pyrogram.raw.base import WebViewResult
from pyrogram.raw.functions.messages import RequestWebView

from coloredlogs import install
from verboselogs import VerboseLogger, VERBOSE

logger = VerboseLogger('my_logger')
install(level=VERBOSE, fmt='[%(asctime)s] | %(levelname)-6s | %(message)s')

softwares = [SoftwareName.FIREFOX.value]
ost = [OperatingSystem.IOS.value]
sengine = [SoftwareEngine.KHTML.value, SoftwareEngine.GECKO.value, SoftwareEngine.WEBKIT.value]
stype = [SoftwareType.WEB_BROWSER.value]
htype = [HardwareType.MOBILE__PHONE.value, HardwareType.MOBILE.value]
user_agent_rotator = UserAgent(software_names=softwares, operating_systems=ost, hardware_types=htype, software_types=stype, software_engines=sengine, limit=10000)


class hamster:
	def __init__(self, client, loop):
		print("Running into CATS")
		self.client = client
		self.UA = user_agent_rotator.get_random_user_agent()
		self.cats = 0
		self.proxy = self.prox()
		self.loop = loop
		self.referral_code = ""

	def ts(self):
		return round((datetime.now(timezone('UTC'))).timestamp()) - 1


	def get_session_names(self) -> list[str]:
		session_names = glob.glob('*.session')
		session_names = [path.splitext(path.basename(file))[0] for file in session_names]
		return session_names


	def prox(self):
		error = True
		while error:
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
		error = True
		while error:
			try:
				if json is None:
					response = rget(url, headers=headers, proxies=self.proxy)
				else:
					response = rpost(url, headers=headers, json=json, proxies=self.proxy)
				error = False
				return response
			except Exception as e:
				logger.critical(f"Error in Requesting: {e}")
				error = True
				sleep(1)



	def accountLog(self, auth):
		headers = {
		"Host": 'api.catshouse.club',
		"Sec-Ch-Ua": '"Chromium";v="113", "Not-A.Brand";v="24"',
		"Content-Type": 'application/json',
		"Sec-Ch-Ua-Mobile": '?0',
		"Authorization": f'tma {auth}',
		"User-Agent": self.UA,
		"Sec-Ch-Ua-Platform": '"Linux"',
		"Accept": '*/*',
		"Origin": 'https://cats-frontend.tgapps.store',
		"Sec-Fetch-Site": 'cross-site',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Dest": 'empty',
		"Referer": 'https://cats-frontend.tgapps.store/',
		"Accept-Encoding": 'gzip, deflate',
		"Accept-Language": 'en-US,en;q=0.9'}

		response = self.Request("https://api.catshouse.club/user", headers=headers)
		return json(response.text)


	def accountCreate(self, auth, code):
		headers = {
		"Host": 'api.catshouse.club',
		"Content-Length": '2',
		"Sec-Ch-Ua": '"Chromium";v="113", "Not-A.Brand";v="24"',
		"Content-Type": 'application/json',
		"Sec-Ch-Ua-Mobile": '?0',
		"Authorization": f'tma {auth}',
		"User-Agent": self.UA,
		"Sec-Ch-Ua-Platform": '"Linux"',
		"Accept": '*/*',
		"Origin": 'https://cats-frontend.tgapps.store',
		"Sec-Fetch-Site": 'cross-site',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Dest": 'empty',
		"Referer": 'https://cats-frontend.tgapps.store/',
		"Accept-Encoding": 'gzip, deflate',
		"Accept-Language": 'en-US,en;q=0.9',}
		
		response = self.Request(f"https://api.catshouse.club/user/create?referral_code={code}", headers=headers, json={})
		return True if "id" in json(response.text) else False

	def acccountTasks(self, auth, group):
		headers= {
		"Host": 'api.catshouse.club',
		"Sec-Ch-Ua": '"Chromium";v="113", "Not-A.Brand";v="24"',
		"Content-Type": 'application/json',
		"Sec-Ch-Ua-Mobile": '?0',
		"Authorization": f'tma {auth}',
		"User-Agent": self.UA,
		"Sec-Ch-Ua-Platform": '"Linux"',
		"Accept": '*/*',
		"Origin": 'https://cats-frontend.tgapps.store',
		"Sec-Fetch-Site": 'cross-site',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Dest": 'empty',
		"Referer": 'https://cats-frontend.tgapps.store/',
		"Accept-Encoding": 'gzip, deflate',
		"Accept-Language": 'en-US,en;q=0.',}

		response = self.Request(f"https://api.catshouse.club/tasks/user?group={group}", headers=headers)
		return json(response.text)

	def accountCompleteTask(self, auth, task_id, stats):
		headers = {
		"Host": 'api.catshouse.club',
		"Content-Length": '2',
		"Sec-Ch-Ua": '"Chromium";v="113", "Not-A.Brand";v="24"',
		"Content-Type": 'application/json',
		"Sec-Ch-Ua-Mobile": '?0',
		"Authorization": f'tma {auth}',
		"User-Agent": self.UA,
		"Sec-Ch-Ua-Platform": '"Linux"',
		"Accept": '*/*',
		"Origin": 'https://cats-frontend.tgapps.store',
		"Sec-Fetch-Site": 'cross-site',
		"Sec-Fetch-Mode": 'cors',
		"Sec-Fetch-Dest": 'empty',
		"Referer": 'https://cats-frontend.tgapps.store/',
		"Accept-Encoding": 'gzip, deflate',
		"Accept-Language": 'en-US,en;q=0.9',}
		
		response = self.Request(f"https://api.catshouse.club/tasks/{task_id}/{stats}", headers=headers, json={})
		return json(response.text)

	

	async def run(self):
		try:
			bot_peer = await self.client.resolve_peer("catsgang_bot")

			if (await self.client.get_chat_history_count(bot_peer.user_id)) == 0:
				await self.client.send_message("catsgang_bot", "/start")

			web_view: WebViewResult = await self.client.invoke(RequestWebView(
				peer=bot_peer,
				bot=bot_peer,
				platform="ios",
				url="https://cats-frontend.tgapps.store/",
				start_param=self.referral_code,
				silent=True
				))
			
			auth_data = parse.parse_qs(parse.urlparse(web_view.url).fragment)
			print(auth_data)
			await self.intitalize(auth_data["tgWebAppData"][0])
		except Exception as e:
			logger.warning(e)
			return None

	async def intitalize(self, auth):
		me = await self.client.get_me()
		print(me)
		Log = self.accountLog(auth)
		print(Log)
		if "message" in Log:
			if Log["message"] == "Signature is invalid":
				logger.critical("Invalid Login")

			elif Log["message"] == "User was not found":
				logger.notice(f"Creating Refferal Account... | Invite Code: {self.referral_code}")
				if self.accountCreate(auth, self.referral_code):
					logger.success("Created Reffered Account!")
					Log = self.accountLog(auth)
				else:
					logger.critical(f"Excepitonal Exception Occured! | {Log}")
				
				Log = self.accountLog(auth)
		if "message" not in Log:
			totalPoints = Log['totalRewards']
			logger.success(f"UserID: {Log['id']}")
			logger.success(f"UserName: {Log['username']}")
			logger.success(f"User: {Log['firstName']} {Log['lastName']}")
			logger.success(f"CATS: {Log['totalRewards']}")
			
			n=0
			tasks = self.acccountTasks(auth, "cats")["tasks"]
			for task in tasks:
				try:
					tid = tasks[n]["id"]
					completed = tasks[n]["completed"]
					points = tasks[n]["rewardPoints"]
					title = tasks[n]["title"]
					Ttype = tasks[n]["type"]
					if Ttype == "OPEN_LINK" and (not completed):
						completion = self.accountCompleteTask(auth, tid, "complete")
						if "success" in completion:
							totalPoints += points
							logger.success(f"Completed Task: {title} | Rewards Points: +{points} | Balance: {totalPoints}")
						elif "message" in completion:
							logger.error(f"Unsuccessful Task: {title} | Reason: {completion['message']}")
						else:
							logger.warning(f"Exceptional Task Completion Error! | Issue: {completion}")
					
					if Ttype == "SUBSCRIBE_TO_CHANNEL":
						channel = tasks[n]['params']['channelUrl']
						channel_id = tasks[n]['params']['channelId']
						channel_name = (tasks[n]['params']['channelUrl']).replace('https://t.me/', '')

						try:
							chat_member = await self.client.get_chat_member(channel_id, me.id)
							member = True if chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.LEFT, ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED] else False
						except:
							member = False

						if not completed:
							if not member:
								await self.client.join_chat(channel)
								logger.notice(f"Task: {title} | Joined Channel: {channel_name}")
								sleep(10)
							
							completion = self.accountCompleteTask(auth, tid, "check")
							if "completed" in completion:
								if completion["completed"]:
									totalPoints += points
									logger.success(f"Completed Task: {title} | Rewards Points: +{points} | Balance: {totalPoints}")
									await self.client.leave_chat(channel_id)
									logger.notice(f"Task: {title} | Left Channel: {channel_name}")
								elif not completion["completed"]:
									logger.error(f"Unsuccessful Task: {title}")
								else:
									logger.warning(f"Exceptional Task Completion Error! | Issue: {completion}")

						if completed and member:
							await self.client.leave_chat(channel_id)
							logger.notice(f"Task: {title} | Left Channel: {channel_name}")
					n += 1
				except Exception as e:
					logger.error(e)
					print_exc()
					print(completion)
				finally:
					sleep(5)

			n = 0
			tasks = self.acccountTasks(auth, "bitget")["tasks"]

			for task in tasks:
				try:
					tid = tasks[n]["id"]
					completed = tasks[n]["completed"]
					points = tasks[n]["rewardPoints"]
					title = tasks[n]["title"]
					Ttype = tasks[n]["type"]

					if (Ttype == "OPEN_LINK" or "SUBSCRIBE_TO_CHANNEL") and (not completed):
						completion = self.accountCompleteTask(auth, tid, "complete")
						if "success" in completion:
							totalPoints += points
							logger.success(f"Completed Task: {title} | Rewards Points: +{points} | Balance: {totalPoints}")
						elif "message" in completion:
							logger.error(f"Unsuccessful Task: {title}")
						else:
							logger.warning(f"Exceptional Task Completion Error! | Issue: {completion}")
					n += 1
				except Exception as e:
					logger.error(e)
					print_exc()
					print(completion)
				finally:
					sleep(5)
					
			Log = self.accountLog(auth)
			logger.success(f"SUCCESS | CATS: {Log['totalRewards']}")

	def start(self):
		self.loop.create_task(self.run())