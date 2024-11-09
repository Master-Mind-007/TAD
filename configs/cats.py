#!/usr/bin/env python3

from app import app
from app import db
from sqlalchemy import inspect

from functools import wraps
from sys import setrecursionlimit
from os import path
from glob import glob
from time import sleep, perf_counter
from urllib import parse
from pytz import timezone
from datetime import datetime
from json import loads as json
from traceback import print_exc
from asyncio import sleep as asleep
from random import randint as randomise
from requests import get as rget, post as rpost

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, HardwareType, SoftwareType, SoftwareEngine

from pyrogram.enums import ChatMemberStatus
from pyrogram.raw.base import WebViewResult
from pyrogram.raw.functions.messages import RequestWebView
from pyrogram.errors import FloodWait, BadRequest, RPCError

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


config_name = "cats"
create_db = True
clear_db = False
scheduler = {"time":  12 * 60 * 60}

questionaire = {
	161: "BAKING", # Producitivity Tips!
	160: "ALTCOIN", # Stay Productive
	159: "BAG", # Earn $1000 Just by Listening
	158: "AFFILIATE", # Make Money Online For Free
	154: "AUCTION", # Make 10x Part 2
	155: "AUDIT", # Make 10x Part 3
}


def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper


class CATS(db.Model):
	userid = db.Column(db.Integer, primary_key=True, nullable=False)
	balance = db.Column(db.Integer, nullable=False)

	def __repr__(self) -> str:
		return f"{self.userid} | {self.balance}"
	
class tweak_db:
	def __init__(self) -> None:
		pass
	
	def create_db(self):
		with app.app_context():
			if not inspect(db.engine).has_table(config_name):
				db.create_all()
				logger.notice(f"Created Table {config_name}")
			else:
				if clear_db:
					CATS.__table__.drop(db.engine)
					logger.notice(f"Deleted existing Table {config_name}")
					db.create_all()
	
	@memoize
	def modify(self, userid, balance):
		with app.app_context():
			prev_data = db.session.get(CATS, userid)
			if prev_data:
				prev_data.balance = balance
			else:
				data = CATS(
					userid=int(userid),
					balance = int(balance)
				)
				db.session.add(data)
			db.session.commit()



class cats:
	def __init__(self, client, loop):
		self.client = client
		self.cats = 0
		self.proxy = self.prox()
		self.loop = loop
		self.referral_code = "6w-_x0pAFV_vps-3E3-g9"
		self.UA = user_agent_rotator.get_random_user_agent()
		self.stats = {"status": True, "runs": 0, "success": 0, "fails": 0}
		self.database = tweak_db()

	def ts(self):
		return round((datetime.now(timezone('UTC'))).timestamp()) - 1

	@memoize
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


	@memoize
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


	@memoize
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

	@memoize
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

	@memoize
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

	@memoize
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

	@memoize
	def accountVideoTask(self, auth, task_id, ans):
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
		
		response = self.Request(f"https://api.catshouse.club/tasks/{task_id}/complete?answer={ans}", headers=headers, json={})
		return json(response.text)["success"]
	

	@memoize
	async def run(self):
		if self.stats["status"]:
			try:
				self.stats["runs"] += 1
				self.me = await self.client.get_me()
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
				return await self.intitalize(auth_data["tgWebAppData"][0])
			except FloodWait as e:
				logger.notice(f"FloodWait | Sleeping for {e.value}s")
				await asleep(e.value)
			except (RPCError, BadRequest) as e:
				logger.critical(f"LOGIN: {e}")
				self.stats["fails"] += 1
				return False
			except Exception as e:
				logger.warning(e)
				self.stats["fails"] += 1
				return None


	@memoize
	async def intitalize(self, auth):
		if self.stats["status"]:
			try:
				me = await self.client.get_me()
				Log = self.accountLog(auth)
				if "message" in Log:
					if Log["message"] == "Signature is invalid":
						logger.critical("Invalid Login")

					elif Log["message"] == "User was not found":
						logger.notice(f"Creating Refferal Account... | Invite Code: {self.referral_code}")
						try:
							if self.accountCreate(auth, self.referral_code):
								logger.success("Created Reffered Account!")
								Log = self.accountLog(auth)
							else:
								logger.critical(f"Excepitonal Exception Occured! | {Log}")
						except FloodWait as e:
							logger.notice(f"FloodWait | Sleeping for {e.value}s")
							await asleep(e.value)
						except (RPCError, BadRequest) as e:
							logger.critical(f"Auth APP: {e}")
							return False
						Log = self.accountLog(auth)

				if "message" not in Log:
					totalPoints = Log['totalRewards']
					logger.success(f"UserID: {Log['id']}")
					logger.success(f"UserName: {Log['username']}")
					logger.success(f"User: {Log['firstName']} {Log['lastName']}")
					logger.success(f"CATS: {Log['totalRewards']}")

					self.database.modify(self.me.id, totalPoints)
					
					n=0
					tasks = self.acccountTasks(auth, "cats")["tasks"]
					for task in tasks:
						try:
							tid = tasks[n]["id"]
							completed = tasks[n]["completed"]
							points = tasks[n]["rewardPoints"]
							title = tasks[n]["title"]
							Ttype = tasks[n]["type"]

							if not completed:
								if Ttype == "OPEN_LINK":
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
									member = False

									try:
										chat = await self.client.get_chat(channel_name if '+' not in channel else channel)
										chat_member = await self.client.get_chat_member(chat.id, me.id)
										member = isinstance(chat_member.status, ChatMemberStatus)
										if not member and not completed:
											await self.client.join_chat(chat.id) if '+' not in channel else await self.client.join_chat(channel)
											logger.notice(f"Task: {title} | Joined Channel: {channel_name}")
											sleep(10)
									except RPCError as e:
										if "USER_NOT_PARTICIPANT" in str(e) and not completed:
											await self.client.join_chat(chat.id) if '+' not in channel else await self.client.join_chat(channel)
											logger.notice(f"Task: {title} | Joined Channel: {channel_name}")
											member = True
											sleep(10)
									except Exception as e:
										logger.error(f"Chat Membership Error: {e}")

									try:
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
									except FloodWait as e:
										logger.notice(f"FloodWait | Sleeping for {e.value}s")
										await asleep(e.value)
									except (RPCError, BadRequest) as e:
										logger.critical(f"APP TASK: {e}")
										

								if Ttype == "YOUTUBE_WATCH":
									if tid in questionaire:
										if self.accountVideoTask(auth, tid, questionaire[tid]):
											logger.success(f"Completed Video Task: {title} | Rewards Points: +{points}")
											sleep(5)

							if completed and Ttype == "SUBSCRIBE_TO_CHANNEL":
								try:
									await self.client.leave_chat(channel_id)
									logger.notice(f"Task: {title} | Left Channel: {channel_name}")
								except Exception as e:
									pass

							n += 1
						except Exception as e:
							logger.error(e)
							print_exc()
						finally:
							sleep(5)


					for ex in ["bitget", "kukoin"]:
						n = 0
						extasks = self.acccountTasks(auth, ex)["tasks"]
						for task in extasks:
							try:
								tid = extasks[n]["id"]
								completed = extasks[n]["completed"]
								points = extasks[n]["rewardPoints"]
								title = extasks[n]["title"]
								Ttype = extasks[n]["type"]

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
							finally:
								sleep(5)

							
					Log = self.accountLog(auth)
					logger.success(f"SUCCESS | CATS: {Log['totalRewards']}")
					self.database.modify(self.me.id, Log['totalRewards'])
					self.stats["success"] += 1
					return True
			except FloodWait as e:
				logger.notice(f"FloodWait | Sleeping for {e.value}s")
				await asleep(e.value)
			except (RPCError, BadRequest) as e:
				self.stats["fails"] += 1
				logger.critical(f"INITIALISE: {e}")
				return False
			except Exception as e:
				self.stats["fails"] += 1
				logger.error(f"Initialise Exception: {e}")
				print_exc()

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
	
	@memoize
	def status(self):
		return self.stats

@memoize
def balance():
	with app.app_context():
		return sum([cat.balance for cat in CATS.query.all()])

def generate_db():
	if create_db:
		database = tweak_db()
		database.create_db()
