import yaml
import logging
from pydantic import BaseModel, ValidationError, model_validator
from typing import Optional


class ProxyConfig(BaseModel):
    enable: bool = False
    type: Optional[str] = "http"
    hostname: Optional[str] = "127.0.0.1"
    port: Optional[int] = 12345
    username: Optional[str] = None
    password: Optional[str] = None

    # noinspection PyNestedDecorators
    @model_validator(mode='after')
    @classmethod
    def check_proxy_config(cls, values):
        if values.enable:
            proxy_type = values.type
            if proxy_type not in ['http', 'socks5', 'mtproto']:
                raise ValueError(f"不支持的代理类型: {proxy_type}")
        return values


class BotConfig(BaseModel):
    name: str
    type: str = "userbot"
    bot_token: Optional[str] = None
    api_id: str
    api_hash: str
    debug: bool = False
    test_mode: bool = False

    # noinspection PyNestedDecorators
    @model_validator(mode='after')
    @classmethod
    def check_bot_config(cls, values):
        if values.type == 'bot' and not values.bot_token:
            raise ValueError("Bot 类型为 bot 时必须设置 bot_token 参数")
        elif values.type == 'userbot' and values.bot_token:
            logging.warning("Bot 类型为 userbot 时不需要设置 bot_token 参数，已自动缺省")
            values['bot_token'] = None
        return values


class Config(BaseModel):
    bot: BotConfig
    proxy: ProxyConfig = ProxyConfig()
    time_zone: str = "Asia/ShangHai"
    log_level: str = "INFO"
    debug: bool = False
    ipv6: bool = False

    # noinspection PyNestedDecorators
    @model_validator(mode='after')
    @classmethod
    def check_log_level(cls, values):
        log_level = values.log_level
        if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError("日志级别不支持，仅支持 DEBUG, INFO, WARNING, ERROR, CRITICAL 参数")
        return values


def load_config(filename: str = 'config.yml') -> Config:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return Config(**data)
    except FileNotFoundError:
        logging.critical("配置文件不存在")
        raise
    except yaml.YAMLError:
        logging.critical("配置文件格式错误")
        raise
    except ValidationError as e:
        logging.critical(f"配置文件缺少关键配置项或格式错误: {e}")
        raise


config = load_config()
