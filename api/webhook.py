import json
from main import bot  # import your bot instance
from flask import Request, Response

def handler(request: Request):
    try:
        data = request.get_json()
        if data:
            bot.process_new_updates([data])
        return Response("ok", status=200)
    except Exception as e:
        return Response(str(e), status=500)
