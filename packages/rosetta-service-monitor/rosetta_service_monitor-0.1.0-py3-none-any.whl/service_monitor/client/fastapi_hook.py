#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: xl
@file: fastapi_hook.py 
@time: 2021/08/09
@contact: 
@site:  
@software: PyCharm 
"""
import traceback

from rosetta_service_monitor.client.service.mq_service import mq_serveice


def register_hook(app, project_name) -> None:
    """
    请求响应拦截 hook
    https://fastapi.tiangolo.com/tutorial/middleware/
    :param app:
    :return:
    """

    @app.middleware("http")
    async def logger_request(request, call_next):
        path = request.url.path
        try:
            response = await call_next(request)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as err:
            info = f'{err}:{err.__class__.__name__}\n{traceback.format_exc()}'
            request_data = {
                'path': path,
                'body': request.body(),
                'query_params': request.query_params,
                'form': request.form()
            }
            mq_serveice.send_mq(project_name=project_name, err_msg=info, trace_id='', request=request_data)
            raise err
        return response
