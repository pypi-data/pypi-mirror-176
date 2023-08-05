import orjson
import pydantic
from pydantic import BaseModel
from typing import Union, Optional, Literal
from pathlib import Path
from dotenv import load_dotenv
import os


def orjson_dumps(v, *, default)->str:#type: ignore
    return orjson.dumps(v, default=default).decode()
pydantic.config.BaseConfig.json_loads=orjson.loads
pydantic.config.BaseConfig.json_dumps=orjson_dumps

BASE_DIR = Path(__file__).parent.__str__()
DEBUG=False
MODE=os.getenv("MODE","dev")

if MODE=='dev':
    DEBUG = True
    load_dotenv(os.path.join(BASE_DIR, 'environment/DEV.env'))
    load_dotenv(os.path.join(BASE_DIR, 'environment/DEV.LOCAL.env'))
elif MODE=='stage':
    if os.getenv('KUBERNETES_SERVICE_HOST',None):#run in k8s,load k8s config
        load_dotenv(os.path.join(BASE_DIR, 'environment/STAGE.K8S.env'))
        # calc node id from hostname
        nodeid=sum([ord[i] for i in os.getenv('HOSTNAME').split('-')[-1]])#type: ignore
        os.environ['NODEID']=str(nodeid)
    else:
        load_dotenv(os.path.join(BASE_DIR, 'environment/STAGE.env'))
else:
    if os.getenv('KUBERNETES_SERVICE_HOST', None):  # run in k8s,load k8s config
        load_dotenv(os.path.join(BASE_DIR, 'environment/PROD.K8S.env'))
        nodeid = sum([ord[i] for i in os.getenv('HOSTNAME').split('-')[-1]])#type: ignore
        os.environ['NODEID'] = str(nodeid)
    else:
        load_dotenv(os.path.join(BASE_DIR, 'environment/PROD.env'))
from UserRole import UserRole
NODEID=int(os.getenv("NODEID", 0))
REDISURL:str=os.getenv('REDISURL','')
SLAVEREDISURL:str=os.getenv('SLAVEREDISURL','')
CELERY_BROKER_URL=os.getenv('AMQPURL',REDISURL)
CELERY_RESULT_BACKEND=os.getenv('REDISURL','')
CELERY_RESULT_EXPIRED=3600
WISH_BASEURL=os.getenv("WISH_BASEURL","")
WISH_CLIENTID=os.getenv("WISH_CLIENTID",'')
WISH_SECRET=os.getenv("WISH_SECRET","")
WISH_REDIRECT_URL=os.getenv("WISH_REDIRECT_URL","")
WISH_CODE=os.getenv("WISH_CODE","")
TIKTOK_APPKEY=os.getenv('TIKTOK_APPKEY','')
TIKTOK_SECRET=os.getenv('TIKTOK_SECRET','')

ELASTICSEARCHURL=os.getenv('ELASTICSEARCHURL','')

DBURL=os.getenv("ASYNCDBURL",'')
SLAVEDBURL=os.getenv("SLAVEDBURL",DBURL)
SYNC_DBURL=os.getenv("SYNCDBURL",'')
AUTO_TRUNCATE_COLUMN=os.getenv('AUTO_TRUNCATE_COLUMN',False)

AZ_BLOB_CONNSTR=os.getenv('az_blob_connstr','')
FILE_STORETYPE=os.getenv('FILE_STORETYPE','LOCAL')
ENABLE_CACHE=True
CACHE_PREFIX='xtcache'
DEFAULT_CACHE_EXPIRE=3600*12

TIKTOK_APIURL=os.getenv('TIKTOK_APIURL','https://open-api.tiktokglobalshop.com')
ONBUY_APIURL=os.getenv('ONBUY_APIURL','https://api.onbuy.com/v2')
not_cache_models=['User']
SECRET_KEY = "11a60e557ae59d6a4674bb5aeddcbc963bed0a4d44694f62c3be578d4155471d"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600*3 if MODE!='dev' else 3600*24*90
REFRESH_TOKEN_EXPIRE_SECONDS= 3600*24*15

ALGORITHM = "HS256"
AZCONTAINER_NAMES=Literal['productimage','categoryimg','deitalimage','commonfile']
AZCONTAINER_CONFIG={
'productimage':{
    'resize':[(100,100),(50,50)]

}
}
import enum
class SupportLang(enum.Enum):
    en='en'
    cn='cn'
class UserTokenData(BaseModel):
    id:int
    phone:str=''
    userrole:int=0
    username=''
    nickname:Optional[str]=''
    is_guest=False
    enterprise_id=0
    exp:int=0
    @property
    def is_admin(self)->int:
        if not self.userrole:
            self.userrole=0
        return self.userrole & UserRole.admin.value
    class Config:
        orm_mode = True
