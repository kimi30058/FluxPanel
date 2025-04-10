from fastapi import FastAPI, Form, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import base64
import io
import random
import string
import time
from PIL import Image, ImageDraw
import json
import uuid
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = {
    "admin": {
        "password": "admin123",
        "user_id": 1,
        "username": "admin",
        "nickname": "管理员",
        "dept_id": 100,
        "roles": ["admin"],
        "permissions": ["*:*:*"]
    }
}

tokens = {}

providers = [
    {"id": 1, "name": "OpenAI", "type": "openai", "api_key": "sk-xxx", "api_host": "https://api.openai.com", "enabled": True},
    {"id": 2, "name": "Anthropic", "type": "anthropic", "api_key": "sk-ant-xxx", "api_host": "https://api.anthropic.com", "enabled": True},
    {"id": 3, "name": "Google", "type": "google", "api_key": "aip-xxx", "api_host": "https://generativelanguage.googleapis.com", "enabled": True}
]

models = [
    {"id": 1, "name": "gpt-4", "provider_id": 1, "group": "GPT-4", "types": ["text", "vision", "function"]},
    {"id": 2, "name": "gpt-3.5-turbo", "provider_id": 1, "group": "GPT-3.5", "types": ["text"]},
    {"id": 3, "name": "claude-3-opus", "provider_id": 2, "group": "Claude 3", "types": ["text", "vision"]},
    {"id": 4, "name": "claude-3-sonnet", "provider_id": 2, "group": "Claude 3", "types": ["text", "vision"]},
    {"id": 5, "name": "gemini-pro", "provider_id": 3, "group": "Gemini", "types": ["text"]}
]

assistants = [
    {"id": 1, "name": "通用助手", "prompt": "你是一个有用的AI助手", "type": "general", "emoji": "🤖", "model_id": 1},
    {"id": 2, "name": "代码助手", "prompt": "你是一个编程专家", "type": "code", "emoji": "💻", "model_id": 1},
    {"id": 3, "name": "翻译助手", "prompt": "你是一个翻译专家", "type": "translation", "emoji": "🌐", "model_id": 2}
]

topics = [
    {"id": 1, "name": "关于Python的讨论", "assistant_id": 2, "created_at": "2023-01-01T00:00:00"},
    {"id": 2, "name": "AI发展趋势", "assistant_id": 1, "created_at": "2023-01-02T00:00:00"}
]

messages = [
    {"id": 1, "topic_id": 1, "role": "user", "content": "Python和JavaScript有什么区别？", "created_at": "2023-01-01T00:00:00"},
    {"id": 2, "topic_id": 1, "role": "assistant", "content": "Python和JavaScript有很多区别...", "created_at": "2023-01-01T00:00:01"}
]

knowledge_bases = [
    {"id": 1, "name": "编程知识库", "description": "包含各种编程语言的知识", "model_id": 1}
]

knowledge_items = [
    {"id": 1, "knowledge_base_id": 1, "type": "note", "content": "Python是一种解释型高级编程语言"}
]

def generate_captcha():
    width, height = 100, 40
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    draw.text((10, 10), captcha_text, fill=(0, 0, 0))
    
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return {"img": f"data:image/png;base64,{img_str}", "uuid": str(uuid.uuid4()), "text": captcha_text}

def generate_token(username):
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    expiry = datetime.now() + timedelta(hours=2)
    tokens[token] = {"username": username, "expiry": expiry}
    return token

def verify_token(token):
    if token not in tokens:
        return None
    token_data = tokens[token]
    if token_data["expiry"] < datetime.now():
        del tokens[token]
        return None
    return token_data["username"]

def paginate(items, page_num, page_size):
    start = (page_num - 1) * page_size
    end = start + page_size
    total = len(items)
    
    return {
        "total": total,
        "rows": items[start:min(end, total)],
        "code": 200,
        "msg": "查询成功"
    }

@app.get("/")
async def root():
    return {"message": "Backend server is running"}

@app.post("/captcha")
async def get_captcha():
    captcha = generate_captcha()
    return {
        "code": 200,
        "msg": "操作成功",
        "data": {
            "img": captcha["img"],
            "uuid": captcha["uuid"]
        }
    }

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), code: str = Form(None), uuid: str = Form(None)):
    if username in users and users[username]["password"] == password:
        token = generate_token(username)
        return {
            "code": 200,
            "msg": "操作成功",
            "data": {
                "access_token": token
            }
        }
    else:
        return {
            "code": 500,
            "msg": "用户名或密码错误"
        }

@app.get("/getInfo")
async def get_info(Authorization: Optional[str] = Query(None)):
    if not Authorization:
        return {"code": 401, "msg": "未登录"}
    
    token = Authorization.replace("Bearer ", "")
    username = verify_token(token)
    
    if not username:
        return {"code": 401, "msg": "登录已过期"}
    
    user = users[username]
    return {
        "code": 200,
        "msg": "操作成功",
        "data": {
            "user": {
                "userId": user["user_id"],
                "username": user["username"],
                "nickname": user["nickname"],
                "deptId": user["dept_id"]
            },
            "roles": user["roles"],
            "permissions": user["permissions"]
        }
    }

@app.get("/getRouters")
async def get_routers(Authorization: Optional[str] = Query(None)):
    if not Authorization:
        return {"code": 401, "msg": "未登录"}
    
    token = Authorization.replace("Bearer ", "")
    username = verify_token(token)
    
    if not username:
        return {"code": 401, "msg": "登录已过期"}
    
    return {
        "code": 200,
        "msg": "操作成功",
        "data": [
            {
                "name": "System",
                "path": "/system",
                "hidden": False,
                "component": "Layout",
                "meta": {"title": "系统管理", "icon": "system"},
                "children": [
                    {
                        "name": "User",
                        "path": "user",
                        "component": "system/user/index",
                        "meta": {"title": "用户管理", "icon": "user"}
                    }
                ]
            },
            {
                "name": "AI",
                "path": "/ai",
                "hidden": False,
                "component": "Layout",
                "meta": {"title": "AI管理", "icon": "ai"},
                "children": [
                    {
                        "name": "Provider",
                        "path": "provider",
                        "component": "ai/provider/index",
                        "meta": {"title": "提供商管理", "icon": "provider"}
                    },
                    {
                        "name": "Model",
                        "path": "model",
                        "component": "ai/model/index",
                        "meta": {"title": "模型管理", "icon": "model"}
                    },
                    {
                        "name": "Assistant",
                        "path": "assistant",
                        "component": "ai/assistant/index",
                        "meta": {"title": "助手管理", "icon": "assistant"}
                    },
                    {
                        "name": "Chat",
                        "path": "chat",
                        "component": "ai/chat/index",
                        "meta": {"title": "对话", "icon": "chat"}
                    }
                ]
            }
        ]
    }

@app.get("/ai/provider/list")
async def get_provider_list(pageNum: int = Query(1), pageSize: int = Query(10)):
    return {"code": 200, "msg": "操作成功", "data": paginate(providers, pageNum, pageSize)}

@app.get("/ai/provider/{provider_id}")
async def get_provider(provider_id: int):
    provider = next((p for p in providers if p["id"] == provider_id), None)
    if not provider:
        return {"code": 404, "msg": "提供商不存在"}
    return {"code": 200, "msg": "操作成功", "data": provider}

@app.post("/ai/provider")
async def add_provider(provider: Dict[str, Any]):
    provider_id = max(p["id"] for p in providers) + 1
    provider["id"] = provider_id
    providers.append(provider)
    return {"code": 200, "msg": "操作成功", "data": provider}

@app.put("/ai/provider")
async def update_provider(provider: Dict[str, Any]):
    provider_id = provider.get("id")
    if not provider_id:
        return {"code": 400, "msg": "提供商ID不能为空"}
    
    for i, p in enumerate(providers):
        if p["id"] == provider_id:
            providers[i] = provider
            return {"code": 200, "msg": "操作成功", "data": provider}
    
    return {"code": 404, "msg": "提供商不存在"}

@app.delete("/ai/provider/{provider_ids}")
async def delete_provider(provider_ids: str):
    id_list = [int(id) for id in provider_ids.split(",")]
    global providers
    providers = [p for p in providers if p["id"] not in id_list]
    return {"code": 200, "msg": "操作成功"}

@app.get("/ai/model/list")
async def get_model_list(pageNum: int = Query(1), pageSize: int = Query(10)):
    return {"code": 200, "msg": "操作成功", "data": paginate(models, pageNum, pageSize)}

@app.get("/ai/model/{model_id}")
async def get_model(model_id: int):
    model = next((m for m in models if m["id"] == model_id), None)
    if not model:
        return {"code": 404, "msg": "模型不存在"}
    return {"code": 200, "msg": "操作成功", "data": model}

@app.post("/ai/model")
async def add_model(model: Dict[str, Any]):
    model_id = max(m["id"] for m in models) + 1
    model["id"] = model_id
    models.append(model)
    return {"code": 200, "msg": "操作成功", "data": model}

@app.put("/ai/model")
async def update_model(model: Dict[str, Any]):
    model_id = model.get("id")
    if not model_id:
        return {"code": 400, "msg": "模型ID不能为空"}
    
    for i, m in enumerate(models):
        if m["id"] == model_id:
            models[i] = model
            return {"code": 200, "msg": "操作成功", "data": model}
    
    return {"code": 404, "msg": "模型不存在"}

@app.delete("/ai/model/{model_ids}")
async def delete_model(model_ids: str):
    id_list = [int(id) for id in model_ids.split(",")]
    global models
    models = [m for m in models if m["id"] not in id_list]
    return {"code": 200, "msg": "操作成功"}

@app.get("/ai/assistant/list")
async def get_assistant_list(pageNum: int = Query(1), pageSize: int = Query(10)):
    return {"code": 200, "msg": "操作成功", "data": paginate(assistants, pageNum, pageSize)}

@app.get("/ai/assistant/{assistant_id}")
async def get_assistant(assistant_id: int):
    assistant = next((a for a in assistants if a["id"] == assistant_id), None)
    if not assistant:
        return {"code": 404, "msg": "助手不存在"}
    return {"code": 200, "msg": "操作成功", "data": assistant}

@app.post("/ai/assistant")
async def add_assistant(assistant: Dict[str, Any]):
    assistant_id = max(a["id"] for a in assistants) + 1
    assistant["id"] = assistant_id
    assistants.append(assistant)
    return {"code": 200, "msg": "操作成功", "data": assistant}

@app.put("/ai/assistant")
async def update_assistant(assistant: Dict[str, Any]):
    assistant_id = assistant.get("id")
    if not assistant_id:
        return {"code": 400, "msg": "助手ID不能为空"}
    
    for i, a in enumerate(assistants):
        if a["id"] == assistant_id:
            assistants[i] = assistant
            return {"code": 200, "msg": "操作成功", "data": assistant}
    
    return {"code": 404, "msg": "助手不存在"}

@app.delete("/ai/assistant/{assistant_ids}")
async def delete_assistant(assistant_ids: str):
    id_list = [int(id) for id in assistant_ids.split(",")]
    global assistants
    assistants = [a for a in assistants if a["id"] not in id_list]
    return {"code": 200, "msg": "操作成功"}

@app.get("/ai/topic/list")
async def get_topic_list(pageNum: int = Query(1), pageSize: int = Query(10)):
    return {"code": 200, "msg": "操作成功", "data": paginate(topics, pageNum, pageSize)}

@app.get("/ai/message/list")
async def get_message_list(pageNum: int = Query(1), pageSize: int = Query(10), topicId: Optional[int] = None):
    if topicId:
        filtered_messages = [m for m in messages if m["topic_id"] == topicId]
        return {"code": 200, "msg": "操作成功", "data": paginate(filtered_messages, pageNum, pageSize)}
    return {"code": 200, "msg": "操作成功", "data": paginate(messages, pageNum, pageSize)}

@app.get("/ai/knowledge-base/list")
async def get_knowledge_base_list(pageNum: int = Query(1), pageSize: int = Query(10)):
    return {"code": 200, "msg": "操作成功", "data": paginate(knowledge_bases, pageNum, pageSize)}

@app.get("/ai/knowledge-item/list")
async def get_knowledge_item_list(pageNum: int = Query(1), pageSize: int = Query(10), knowledgeBaseId: Optional[int] = None):
    if knowledgeBaseId:
        filtered_items = [i for i in knowledge_items if i["knowledge_base_id"] == knowledgeBaseId]
        return {"code": 200, "msg": "操作成功", "data": paginate(filtered_items, pageNum, pageSize)}
    return {"code": 200, "msg": "操作成功", "data": paginate(knowledge_items, pageNum, pageSize)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9098)
