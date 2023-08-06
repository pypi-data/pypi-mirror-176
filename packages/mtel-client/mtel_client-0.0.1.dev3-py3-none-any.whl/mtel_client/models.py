from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Currency(BaseModel):
    active: bool = None
    isocode: str = None
    name: str = None
    symbol: str = None


class Language(BaseModel):
    active: bool = None
    isocode: str = None
    name: str = None
    nativeName: str = None


class SubscriptionInfo(BaseModel):
    type: str = None
    customerId: str = None
    description: str = None
    firstName: str = None
    lastName: str = None
    subscriberIdentity: str = None  # Important field for secure requests
    title: str = None


class MtmCustomers(BaseModel):
    additionalServices: List = []
    formattedContactPhone: str = None
    subscriptionInfo: SubscriptionInfo = None


class UserInfo(BaseModel):
    serviceTypes: List[str] = []
    currency: Currency = None
    displayUid: str = None
    firstName: str = None
    lastName: str = None
    language: Language = None
    mtmCustomers: List[MtmCustomers] = None
    name: str = None
    securityCodeActive: bool = None
    uid: EmailStr = None
    uuid: UUID = None


class UserBalance(BaseModel):
    currencyIso: str = None
    formattedValue: str = None
    value: Decimal


class Balance(UserBalance):
    expiredDate: datetime = None
    formattedExpiredDate: str = None


class UserTariffInfo(BaseModel):
    subscriptionType: str = (None,)
    balance: Balance
    headerDescription: str = None
    headerTitle: str = None
    subscriberIdentity: str


class Resource(BaseModel):
    info: str = None
    order: int = None
    remainingValue: str = None
    unitOfMeasure: str = None
    usageType: str = None
    value: str = None


class Service(BaseModel):
    type: str = (None,)
    resources: List[Resource] = []


class UserDetail(BaseModel):
    contractStatus: str = None
    subscriptionState: str = None
    subscriptionType: str = None
    activatedAddons: List = []
    averageServiceUsages: List[Service] = None
    balance: Balance
    customerId: int
    deviceBills: List = []
    hasPersonalizedOffers: bool = None
    headerDescription: str = None
    headerTitle: str = None
    subscriberIdentity: str
