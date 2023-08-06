import asyncio
import logging

import exc
import httpx
from models import UserBalance, UserDetail, UserInfo, UserTariffInfo

BASE_URL = "https://moj.mtel.me/"

MTEL_ENDPOINTS = {
    "auth": "selfcare/b2c/users/authorize",
    "token": "selfcare/b2c/auth/token",
    "user_info": "hybris/selfcare/b2c/v1/user/info",
    "balance": "hybris/selfcare/b2c/v1/user/services/balance",
    "tariff": "hybris/selfcare/b2c/v1/user/service/header",
    "detail": "hybris/selfcare/b2c/v1/user/service/details",
}

logger = logging.getLogger(__name__)


class Profile:
    """
    Getting info about your MTEL (Montenegro) Account!
    Example use:

    data = Profile(email='...', password='...')
    print(data.balance.value)
    >>> 0.8444

    Available user data:
     - short user info: self.user: UserInfo
     - short info about user balance: self.balance: UserBalance
     - info about user tariff: self.tariff: UserTariffInfo
     - detailed info about user self.user_detail: UserDetail

    See models to get more documentaion
    """

    def __init__(
        self, email: str, password: str, cookies=None, token: str = None, loop=None
    ):
        if not loop:
            self.loop = asyncio.get_event_loop()
        self.headers = {}
        self.cookies = cookies  # auth cookies
        self.token = token  # auth token (authorization header)
        self.email = email
        self.password = password
        self.client = httpx.AsyncClient
        self.is_authorized = False

        # endpoints
        self.auth_url = BASE_URL + MTEL_ENDPOINTS["auth"]
        self.token_url = BASE_URL + MTEL_ENDPOINTS["token"]
        self.user_info_url = BASE_URL + MTEL_ENDPOINTS["user_info"]
        self.balance_url = BASE_URL + MTEL_ENDPOINTS["balance"]
        self.tariff_url = BASE_URL + MTEL_ENDPOINTS["tariff"]
        self.detaul_url = BASE_URL + MTEL_ENDPOINTS["detail"]

        # Required field
        self.subscriberIdentity: str = None

        # Data
        self.user: UserInfo = None
        self.balance: UserBalance = None
        self.tariff: UserTariffInfo = None
        self.user_detail: UserDetail = None

        self.loop.run_until_complete(self.auth())
        self.loop.run_until_complete(self.get_data())

    async def auth(self):
        async with self.client() as client:
            await self.get_auth(client=client)
            await self.get_token(client=client)

    async def get_data(self):
        await self.get_user_info(client=self.client)
        self.subscriberIdentity = self.user.mtmCustomers[
            0
        ].subscriptionInfo.subscriberIdentity

        await asyncio.gather(
            self.get_user_balance(client=self.client),
            self.get_user_tariff(client=self.client),
            self.get_user_detail(client=self.client),
        )

    async def get_auth(self, client):
        try:
            resp = await client.post(
                url=self.auth_url,
                data={
                    "userId": self.email,
                    "encodedPassword": self.password,
                    "rememberMe": True,
                },
            )
            if resp.status_code == 400:
                raise exc.WrongCredentialsExc(
                    f"Something wrong with credentials. Status code: {resp.status_code}. Original response: {resp.content}"
                )
            elif resp.status_code != 201:
                raise exc.AuthExc(
                    f"Something wrong with authorization. Status code: {resp.status_code}. Original response: {resp.content}"
                )
            self.is_authorized = True
            self.cookies = client.cookies
            self.headers = client.headers
        except Exception as e:
            logger.exception(e)
            return

    async def get_token(self, client):
        try:
            resp = await client.get(self.token_url)
            if resp.status_code != 200:
                raise exc.GetTokenExc(
                    f"Can't retrieve token, wrong response. Status code: {resp.status_code} Response: {resp.content}"
                )
            self.token = resp.json()["token"]
            self.cookies = client.cookies
            self.headers = {"authorization": self.token, **client.headers}
        except Exception as e:
            logger.exception(e)
            return

    async def get_user_info(self, client=None):
        c = client or self.client
        async with c(cookies=self.cookies, headers=self.headers) as c:
            try:
                resp = await c.get(self.user_info_url)
                if resp.status_code != 200:
                    raise exc.GetUserInfoExc(
                        f"Error getting user info. Status code: {resp.status_code} Response: {resp.content}"
                    )
                self.user = UserInfo(**resp.json())
            except Exception as e:
                logger.exception(e)

    async def get_user_balance(self, client=None):
        c = client or self.client
        async with c(cookies=self.cookies, headers=self.headers) as c:
            try:
                resp = await c.post(
                    self.balance_url,
                    json={"subscriberIdentity": self.subscriberIdentity},
                )
                if resp.status_code != 200:
                    raise exc.GetUserBalanceExc(
                        f"Error getting user balance. Status code: {resp.status_code} Response: {resp.content}"
                    )
                self.balance = UserBalance(**resp.json())
            except Exception as e:
                logger.exception(e)

    async def get_user_tariff(self, client=None):
        c = client or self.client
        async with c(cookies=self.cookies, headers=self.headers) as c:
            try:
                resp = await c.get(
                    self.tariff_url,
                    params={"subscriberIdentity": self.subscriberIdentity},
                )
                if resp.status_code != 200:
                    raise exc.GetUserTariffExc(
                        f"Error getting user tariff. Status code: {resp.status_code} Response: {resp.content}"
                    )
                self.tariff = UserTariffInfo(**resp.json())
            except Exception as e:
                logger.exception(e)

    async def get_user_detail(self, client=None):
        c = client or self.client
        async with c(cookies=self.cookies, headers=self.headers) as c:
            try:
                resp = await c.get(
                    self.detaul_url,
                    params={"subscriberIdentity": self.subscriberIdentity},
                )
                if resp.status_code != 200:
                    raise exc.GetUserDetailExc(
                        f"Error getting user detail data. Status code: {resp.status_code} Response: {resp.content}"
                    )
                self.user_detail = UserDetail(**resp.json())
            except Exception as e:
                logger.exception(e)
