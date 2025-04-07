# RuoYi-FastAPI

RuoYi-FastAPI接口文档

API 版本: 1.6.2

## 基础URL
- /dev-api: 

## API 路径

### AI功能-DIFY集成

#### 发送聊天消息
**操作ID**: `chat_api_ai_dify_chat_post`

**路径**: `/api/ai/dify/chat`
**方法**: `POST`

向DIFY发送聊天消息并获取回复，支持阻塞模式。
        
        - **app_id**: DIFY应用ID
        - **query**: 用户输入/提问内容
        - **conversation_id**: 会话ID，为空则创建新会话
        - **user_id**: 用户标识，由开发者定义规则，需保证用户标识在应用内唯一
        - **streaming**: 是否使用流式返回，对于此接口，请设置为false
        - **inputs**: 允许传入App定义的各变量值
        - **files**: 上传的文件列表
        
        返回结果包含会话ID、消息ID和回复内容。

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: 聊天响应结果

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 流式发送聊天消息
**操作ID**: `chat_stream_api_ai_dify_chat_stream_post`

**路径**: `/api/ai/dify/chat/stream`
**方法**: `POST`

向DIFY发送聊天消息并获取流式回复，适用于需要实时显示回复内容的场景。
        
        返回的是SSE（Server-Sent Events）流，前端需要使用EventSource或其他方式处理流式数据。
        
        每个事件格式为：
        ```
        data: {"event": "message", "message_id": "xxx", "conversation_id": "xxx", "answer": "内容片段"}
        ```
        
        当收到`event: message_end`事件时，表示流式响应结束。

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: SSE流式聊天响应

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 创建聊天会话
**操作ID**: `create_chat_api_ai_dify_chats_post`

**路径**: `/api/ai/dify/chats`
**方法**: `POST`

创建一个新的聊天会话。
        
        - **app_id**: 应用ID
        - **user_id**: 用户ID
        - **title**: 聊天标题，默认为"新聊天"
        
        创建成功后返回会话ID和标题等信息。

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: 创建的聊天会话信息

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 获取用户聊天列表
**操作ID**: `get_user_chats_api_ai_dify_chats_get`

**路径**: `/api/ai/dify/chats`
**方法**: `GET`

获取指定用户的聊天会话列表。
        
        - **user_id**: 用户ID
        - **app_id**: 应用ID（可选，若提供则只返回该应用的聊天）
        - **limit**: 返回条数，默认20条
        - **offset**: 偏移量，默认0
        
        返回的列表按更新时间倒序排列。

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| user_id | query | integer | 是 | 用户ID |
| app_id | query |  | 否 | 应用ID，可选 |
| limit | query | integer | 否 | 返回条数，默认20 |
| offset | query | integer | 否 | 偏移量，默认0 |

**响应**:

**状态码 200**: 用户聊天会话列表

Content-Type: `application/json`

数组项模式:

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 发送消息到现有聊天
**操作ID**: `send_message_api_ai_dify_chats__chat_id__messages_post`

**路径**: `/api/ai/dify/chats/{chat_id}/messages`
**方法**: `POST`

向已存在的聊天会话发送消息。
        
        - **chat_id**: 聊天ID
        - **content**: 消息内容
        - **user_id**: 用户标识
        - **streaming**: 是否使用流式返回
        
        系统会自动保存用户消息和DIFY的回复，并更新聊天元数据。

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| chat_id | path | integer | 是 |  |

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: 发送消息的结果，包含用户消息ID和助手消息ID

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 获取聊天消息列表
**操作ID**: `get_chat_messages_api_ai_dify_chats__chat_id__messages_get`

**路径**: `/api/ai/dify/chats/{chat_id}/messages`
**方法**: `GET`

获取指定聊天会话的消息列表。
        
        - **chat_id**: 聊天ID
        - **limit**: 返回条数，默认20条
        - **offset**: 偏移量，默认0
        
        返回的列表按创建时间升序排列。

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| chat_id | path | integer | 是 |  |
| limit | query | integer | 否 | 返回条数，默认20条 |
| offset | query | integer | 否 | 偏移量，默认0 |

**响应**:

**状态码 200**: 聊天消息列表

Content-Type: `application/json`

数组项模式:

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 删除聊天会话
**操作ID**: `delete_chat_api_ai_dify_chats__chat_id__delete`

**路径**: `/api/ai/dify/chats/{chat_id}`
**方法**: `DELETE`

删除指定的聊天会话。
        
        - **chat_id**: 要删除的聊天ID
        
        删除成功返回{"success": true}。

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| chat_id | path | integer | 是 |  |

**响应**:

**状态码 200**: 删除操作结果

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 重命名聊天会话
**操作ID**: `rename_chat_api_ai_dify_chats__chat_id__title_put`

**路径**: `/api/ai/dify/chats/{chat_id}/title`
**方法**: `PUT`

重命名指定的聊天会话。
        
        - **chat_id**: 聊天ID
        - **title**: 新标题
        
        重命名成功返回更新后的会话信息。

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| chat_id | path | integer | 是 |  |

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: 重命名后的会话信息

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### DeepSeek聊天接口
**操作ID**: `chat_endpoint_api_ai_deepseek_chat_post`

**路径**: `/api/ai/deepseek/chat`
**方法**: `POST`

DeepSeek聊天接口，非流式响应

Args:
    request: 请求参数，包含消息内容、模型参数等
    service: DeepSeek服务实例
    current_user: 当前用户
    db: 数据库会话
    
Returns:
    DeepSeek API响应结果

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| provider_id | query | integer | 是 |  |

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### DeepSeek流式聊天接口
**操作ID**: `chat_stream_endpoint_api_ai_deepseek_chat_stream_post`

**路径**: `/api/ai/deepseek/chat/stream`
**方法**: `POST`

DeepSeek流式聊天接口

Args:
    request: 请求参数，包含消息内容、模型参数等
    service: DeepSeek服务实例
    current_user: 当前用户
    db: 数据库会话
    
Returns:
    流式响应

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| provider_id | query | integer | 是 |  |

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### DeepSeek推理模型接口
**操作ID**: `reasoner_endpoint_api_ai_deepseek_reasoner_post`

**路径**: `/api/ai/deepseek/reasoner`
**方法**: `POST`

DeepSeek-R1推理模型接口

Args:
    request: 请求参数，包含消息内容、模型参数等
    service: DeepSeek服务实例
    current_user: 当前用户
    db: 数据库会话
    
Returns:
    DeepSeek API响应结果

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| provider_id | query | integer | 是 |  |

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 保存DeepSeek聊天记录
**操作ID**: `save_chat_endpoint_api_ai_deepseek_save_chat_post`

**路径**: `/api/ai/deepseek/save_chat`
**方法**: `POST`

保存DeepSeek聊天记录到数据库

Args:
    request: 请求参数，包含聊天记录、应用信息等
    background_tasks: 后台任务
    current_user: 当前用户
    db: 数据库会话
    
Returns:
    保存结果

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### DIFY API

#### 发送聊天消息
**操作ID**: `chat_api_ai_dify_chat_post`

**路径**: `/api/ai/dify/chat`
**方法**: `POST`

向DIFY发送聊天消息并获取回复，支持阻塞模式。
        
        - **app_id**: DIFY应用ID
        - **query**: 用户输入/提问内容
        - **conversation_id**: 会话ID，为空则创建新会话
        - **user_id**: 用户标识，由开发者定义规则，需保证用户标识在应用内唯一
        - **streaming**: 是否使用流式返回，对于此接口，请设置为false
        - **inputs**: 允许传入App定义的各变量值
        - **files**: 上传的文件列表
        
        返回结果包含会话ID、消息ID和回复内容。

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: 聊天响应结果

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 流式发送聊天消息
**操作ID**: `chat_stream_api_ai_dify_chat_stream_post`

**路径**: `/api/ai/dify/chat/stream`
**方法**: `POST`

向DIFY发送聊天消息并获取流式回复，适用于需要实时显示回复内容的场景。
        
        返回的是SSE（Server-Sent Events）流，前端需要使用EventSource或其他方式处理流式数据。
        
        每个事件格式为：
        ```
        data: {"event": "message", "message_id": "xxx", "conversation_id": "xxx", "answer": "内容片段"}
        ```
        
        当收到`event: message_end`事件时，表示流式响应结束。

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: SSE流式聊天响应

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 创建聊天会话
**操作ID**: `create_chat_api_ai_dify_chats_post`

**路径**: `/api/ai/dify/chats`
**方法**: `POST`

创建一个新的聊天会话。
        
        - **app_id**: 应用ID
        - **user_id**: 用户ID
        - **title**: 聊天标题，默认为"新聊天"
        
        创建成功后返回会话ID和标题等信息。

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: 创建的聊天会话信息

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 获取用户聊天列表
**操作ID**: `get_user_chats_api_ai_dify_chats_get`

**路径**: `/api/ai/dify/chats`
**方法**: `GET`

获取指定用户的聊天会话列表。
        
        - **user_id**: 用户ID
        - **app_id**: 应用ID（可选，若提供则只返回该应用的聊天）
        - **limit**: 返回条数，默认20条
        - **offset**: 偏移量，默认0
        
        返回的列表按更新时间倒序排列。

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| user_id | query | integer | 是 | 用户ID |
| app_id | query |  | 否 | 应用ID，可选 |
| limit | query | integer | 否 | 返回条数，默认20 |
| offset | query | integer | 否 | 偏移量，默认0 |

**响应**:

**状态码 200**: 用户聊天会话列表

Content-Type: `application/json`

数组项模式:

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 发送消息到现有聊天
**操作ID**: `send_message_api_ai_dify_chats__chat_id__messages_post`

**路径**: `/api/ai/dify/chats/{chat_id}/messages`
**方法**: `POST`

向已存在的聊天会话发送消息。
        
        - **chat_id**: 聊天ID
        - **content**: 消息内容
        - **user_id**: 用户标识
        - **streaming**: 是否使用流式返回
        
        系统会自动保存用户消息和DIFY的回复，并更新聊天元数据。

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| chat_id | path | integer | 是 |  |

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: 发送消息的结果，包含用户消息ID和助手消息ID

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 获取聊天消息列表
**操作ID**: `get_chat_messages_api_ai_dify_chats__chat_id__messages_get`

**路径**: `/api/ai/dify/chats/{chat_id}/messages`
**方法**: `GET`

获取指定聊天会话的消息列表。
        
        - **chat_id**: 聊天ID
        - **limit**: 返回条数，默认20条
        - **offset**: 偏移量，默认0
        
        返回的列表按创建时间升序排列。

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| chat_id | path | integer | 是 |  |
| limit | query | integer | 否 | 返回条数，默认20条 |
| offset | query | integer | 否 | 偏移量，默认0 |

**响应**:

**状态码 200**: 聊天消息列表

Content-Type: `application/json`

数组项模式:

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 删除聊天会话
**操作ID**: `delete_chat_api_ai_dify_chats__chat_id__delete`

**路径**: `/api/ai/dify/chats/{chat_id}`
**方法**: `DELETE`

删除指定的聊天会话。
        
        - **chat_id**: 要删除的聊天ID
        
        删除成功返回{"success": true}。

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| chat_id | path | integer | 是 |  |

**响应**:

**状态码 200**: 删除操作结果

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 重命名聊天会话
**操作ID**: `rename_chat_api_ai_dify_chats__chat_id__title_put`

**路径**: `/api/ai/dify/chats/{chat_id}/title`
**方法**: `PUT`

重命名指定的聊天会话。
        
        - **chat_id**: 聊天ID
        - **title**: 新标题
        
        重命名成功返回更新后的会话信息。

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| chat_id | path | integer | 是 |  |

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: 重命名后的会话信息

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### DeepSeek API

#### DeepSeek聊天接口
**操作ID**: `chat_endpoint_api_ai_deepseek_chat_post`

**路径**: `/api/ai/deepseek/chat`
**方法**: `POST`

DeepSeek聊天接口，非流式响应

Args:
    request: 请求参数，包含消息内容、模型参数等
    service: DeepSeek服务实例
    current_user: 当前用户
    db: 数据库会话
    
Returns:
    DeepSeek API响应结果

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| provider_id | query | integer | 是 |  |

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### DeepSeek流式聊天接口
**操作ID**: `chat_stream_endpoint_api_ai_deepseek_chat_stream_post`

**路径**: `/api/ai/deepseek/chat/stream`
**方法**: `POST`

DeepSeek流式聊天接口

Args:
    request: 请求参数，包含消息内容、模型参数等
    service: DeepSeek服务实例
    current_user: 当前用户
    db: 数据库会话
    
Returns:
    流式响应

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| provider_id | query | integer | 是 |  |

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### DeepSeek推理模型接口
**操作ID**: `reasoner_endpoint_api_ai_deepseek_reasoner_post`

**路径**: `/api/ai/deepseek/reasoner`
**方法**: `POST`

DeepSeek-R1推理模型接口

Args:
    request: 请求参数，包含消息内容、模型参数等
    service: DeepSeek服务实例
    current_user: 当前用户
    db: 数据库会话
    
Returns:
    DeepSeek API响应结果

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| provider_id | query | integer | 是 |  |

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 保存DeepSeek聊天记录
**操作ID**: `save_chat_endpoint_api_ai_deepseek_save_chat_post`

**路径**: `/api/ai/deepseek/save_chat`
**方法**: `POST`

保存DeepSeek聊天记录到数据库

Args:
    request: 请求参数，包含聊天记录、应用信息等
    background_tasks: 后台任务
    current_user: 当前用户
    db: 数据库会话
    
Returns:
    保存结果

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`
