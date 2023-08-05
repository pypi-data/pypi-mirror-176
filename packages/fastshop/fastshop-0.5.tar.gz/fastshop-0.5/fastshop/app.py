import settings
from common.getSiteInfo import getSiteInfo
import Models
if settings.MODE=='dev':
    import subprocess
    import sys
    subprocess.Popen([sys.executable, "devtools/debugtools.py"],stdout=subprocess.DEVNULL,stdin=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True)

import fastapi.exceptions
import asyncio
import os
from sqlalchemy.exc import IntegrityError,OperationalError
import importlib
from typing import Any
from fastapi import FastAPI, Request, Depends
from redis.exceptions import ConnectionError
from XTTOOLS import cache,snowFlack,Common500Response, TokenException, PermissionException,XTJsonResponse
from pathlib import Path
from common.globalFunctions import writelog
from common.globalFunctions import getorgeneratetoken, get_token
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
if os.name!='nt':
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
else:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from starlette.background import BackgroundTask

app = FastAPI(redoc_url=None if settings.MODE=='main' else '/redoc',docs_url=None if settings.MODE=='main' else '/docs',openapi_url=None if settings.MODE=='main'  else '/openapi.json')
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

@app.middleware("http")
async def validate_tokenandperformevent(request: Request, call_next:Any)->Response:
    #todo: need verify the token expire date.and add refresh token.
    request.state.token=await getorgeneratetoken(request)
    request.state.siteinfo={"lang":"en","domainname":"english.com"}


    try:
        response = await call_next(request)  # This request will be modified and sent
        if db_client:=request.state._state.get('db_client',None):
            await db_client.session.commit()
            backgroundtasks = BackgroundTask(db_client.__aexit__,skipcommit=True)
            response.background =backgroundtasks
    except OperationalError as e:
        jsonout = Common500Response(status='dberror',msg=str(e))
        response=XTJsonResponse(jsonout,status_code=500)
        # try:
        #     await request.state.db_client.close()
        # except:
        #     pass
    except IntegrityError as e:
        await db_client.session.rollback()
        jsonout = Common500Response(status='dberror', msg=str(e))
        response=XTJsonResponse(jsonout,status_code=500)
        # try:
        #     await request.state.db_client.close()
        # except:
        #     pass
    except TokenException as e:

        jsonout = Common500Response(status='tokenerror', msg=str(e))
        response=XTJsonResponse(jsonout,status_code=500)
    except PermissionException as e:
        jsonout = Common500Response(status='permissiondenied', msg=str(e))
        response=XTJsonResponse(jsonout,status_code=500)
    except fastapi.exceptions.ValidationError as e:
        jsonout = Common500Response(status='validateerror',msg='',data=e.errors())
        response=XTJsonResponse(jsonout,status_code=500)
    except  ConnectionError as e:
        jsonout = Common500Response(status='cacheerror',msg='cache server error',data=str(e))
        response=XTJsonResponse(jsonout,status_code=500)
    except Exception as e:
        #es
        print(e)
        await writelog(str(e),request=str(request))

        if settings.DEBUG:
            raise

        jsonout = Common500Response(status='unknownerr', msg=str(e))
        response=XTJsonResponse(jsonout,status_code=500)

    #if request.state.token.is_guest:
    #    response.set_cookie('token',Service.userService.create_access_token(request.state.token),expires=3600*24*30)
    return response

@app.on_event("startup")
async def startup()->None:
    cache.init(prefix=settings.CACHE_PREFIX,expire=settings.DEFAULT_CACHE_EXPIRE,enable=settings.ENABLE_CACHE,
               writeurl=settings.REDISURL,
               readurl=settings.SLAVEREDISURL,
               ignore_arg_types=[settings.UserTokenData],
               )
    snowFlack.init(settings.NODEID)


for f in Path(settings.BASE_DIR).joinpath('modules').rglob('*.py'):
    if f.name.endswith('Controller.py'):
        controller = importlib.import_module(
            str(f.relative_to(settings.BASE_DIR)).replace(os.sep,'.')[0:-3]
        )

        app.include_router(controller.router,prefix='/api')
if not settings.AZ_BLOB_CONNSTR:
    from fastapi.staticfiles import StaticFiles
    app.mount("/img", StaticFiles(directory="img"), name="img")



@app.post('/')
async def forazureping(request:Request, site: "Models.Site" =Depends(getSiteInfo))->dict:

    print(request.headers)
    print(await request.json())
    return {"status": 'success','hello':'world'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info",reload=settings.DEBUG)