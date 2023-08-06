# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cmc_currency_info_response_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class CoinClass:
    id: int
    name: str
    symbol: str
    slug: str
    token_address: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CoinClass':
        assert isinstance(obj, dict)
        id = int(from_str(obj.get("id")))
        name = from_str(obj.get("name"))
        symbol = from_str(obj.get("symbol"))
        slug = from_str(obj.get("slug"))
        token_address = from_union([from_str, from_none], obj.get("token_address"))
        return CoinClass(id, name, symbol, slug, token_address)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(str(self.id))
        result["name"] = from_str(self.name)
        result["symbol"] = from_str(self.symbol)
        result["slug"] = from_str(self.slug)
        result["token_address"] = from_union([from_str, from_none], self.token_address)
        return result


@dataclass
class ContractAddressPlatform:
    name: str
    coin: CoinClass

    @staticmethod
    def from_dict(obj: Any) -> 'ContractAddressPlatform':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        coin = CoinClass.from_dict(obj.get("coin"))
        return ContractAddressPlatform(name, coin)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["coin"] = to_class(CoinClass, self.coin)
        return result


@dataclass
class ContractAddress:
    contract_address: str
    platform: ContractAddressPlatform

    @staticmethod
    def from_dict(obj: Any) -> 'ContractAddress':
        assert isinstance(obj, dict)
        contract_address = from_str(obj.get("contract_address"))
        platform = ContractAddressPlatform.from_dict(obj.get("platform"))
        return ContractAddress(contract_address, platform)

    def to_dict(self) -> dict:
        result: dict = {}
        result["contract_address"] = from_str(self.contract_address)
        result["platform"] = to_class(ContractAddressPlatform, self.platform)
        return result


@dataclass
class Urls:
    website: List[str]
    twitter: List[str]
    message_board: List[Any]
    chat: List[str]
    facebook: List[Any]
    explorer: List[str]
    reddit: List[str]
    technical_doc: List[str]
    source_code: List[str]
    announcement: List[Any]

    @staticmethod
    def from_dict(obj: Any) -> 'Urls':
        assert isinstance(obj, dict)
        website = from_list(from_str, obj.get("website"))
        twitter = from_list(from_str, obj.get("twitter"))
        message_board = from_list(lambda x: x, obj.get("message_board"))
        chat = from_list(from_str, obj.get("chat"))
        facebook = from_list(lambda x: x, obj.get("facebook"))
        explorer = from_list(from_str, obj.get("explorer"))
        reddit = from_list(from_str, obj.get("reddit"))
        technical_doc = from_list(from_str, obj.get("technical_doc"))
        source_code = from_list(from_str, obj.get("source_code"))
        announcement = from_list(lambda x: x, obj.get("announcement"))
        return Urls(website, twitter, message_board, chat, facebook, explorer, reddit, technical_doc, source_code, announcement)

    def to_dict(self) -> dict:
        result: dict = {}
        result["website"] = from_list(from_str, self.website)
        result["twitter"] = from_list(from_str, self.twitter)
        result["message_board"] = from_list(lambda x: x, self.message_board)
        result["chat"] = from_list(from_str, self.chat)
        result["facebook"] = from_list(lambda x: x, self.facebook)
        result["explorer"] = from_list(from_str, self.explorer)
        result["reddit"] = from_list(from_str, self.reddit)
        result["technical_doc"] = from_list(from_str, self.technical_doc)
        result["source_code"] = from_list(from_str, self.source_code)
        result["announcement"] = from_list(lambda x: x, self.announcement)
        return result


@dataclass
class CmcCurrencyInfoResponse:
    id: int
    name: str
    symbol: str
    category: str
    description: str
    slug: str
    logo: str
    subreddit: str
    notice: str
    tags: List[str]
    tag_names: List[str]
    tag_groups: List[str]
    urls: Urls
    platform: CoinClass
    date_added: datetime
    twitter_username: str
    is_hidden: int
    date_launched: None
    contract_address: List[ContractAddress]
    self_reported_circulating_supply: None
    self_reported_tags: None
    self_reported_market_cap: None

    @staticmethod
    def from_dict(obj: Any) -> 'CmcCurrencyInfoResponse':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        symbol = from_str(obj.get("symbol"))
        category = from_str(obj.get("category"))
        description = from_str(obj.get("description"))
        slug = from_str(obj.get("slug"))
        logo = from_str(obj.get("logo"))
        subreddit = from_str(obj.get("subreddit"))
        notice = from_str(obj.get("notice"))
        tags = from_list(from_str, obj.get("tags"))
        tag_names = from_list(from_str, obj.get("tag-names"))
        tag_groups = from_list(from_str, obj.get("tag-groups"))
        urls = Urls.from_dict(obj.get("urls"))
        platform = CoinClass.from_dict(obj.get("platform"))
        date_added = from_datetime(obj.get("date_added"))
        twitter_username = from_str(obj.get("twitter_username"))
        is_hidden = from_int(obj.get("is_hidden"))
        date_launched = from_none(obj.get("date_launched"))
        contract_address = from_list(ContractAddress.from_dict, obj.get("contract_address"))
        self_reported_circulating_supply = from_none(obj.get("self_reported_circulating_supply"))
        self_reported_tags = from_none(obj.get("self_reported_tags"))
        self_reported_market_cap = from_none(obj.get("self_reported_market_cap"))
        return CmcCurrencyInfoResponse(id, name, symbol, category, description, slug, logo, subreddit, notice, tags, tag_names, tag_groups, urls, platform, date_added, twitter_username, is_hidden, date_launched, contract_address, self_reported_circulating_supply, self_reported_tags, self_reported_market_cap)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["symbol"] = from_str(self.symbol)
        result["category"] = from_str(self.category)
        result["description"] = from_str(self.description)
        result["slug"] = from_str(self.slug)
        result["logo"] = from_str(self.logo)
        result["subreddit"] = from_str(self.subreddit)
        result["notice"] = from_str(self.notice)
        result["tags"] = from_list(from_str, self.tags)
        result["tag-names"] = from_list(from_str, self.tag_names)
        result["tag-groups"] = from_list(from_str, self.tag_groups)
        result["urls"] = to_class(Urls, self.urls)
        result["platform"] = to_class(CoinClass, self.platform)
        result["date_added"] = self.date_added.isoformat()
        result["twitter_username"] = from_str(self.twitter_username)
        result["is_hidden"] = from_int(self.is_hidden)
        result["date_launched"] = from_none(self.date_launched)
        result["contract_address"] = from_list(lambda x: to_class(ContractAddress, x), self.contract_address)
        result["self_reported_circulating_supply"] = from_none(self.self_reported_circulating_supply)
        result["self_reported_tags"] = from_none(self.self_reported_tags)
        result["self_reported_market_cap"] = from_none(self.self_reported_market_cap)
        return result


def cmc_currency_info_response_from_dict(s: Any) -> CmcCurrencyInfoResponse:
    return CmcCurrencyInfoResponse.from_dict(s)


def cmc_currency_info_response_to_dict(x: CmcCurrencyInfoResponse) -> Any:
    return to_class(CmcCurrencyInfoResponse, x)
