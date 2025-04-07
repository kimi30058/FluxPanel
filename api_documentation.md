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

---

### 产品官网

#### Home Page
**操作ID**: `home_page__get`

**路径**: `/`
**方法**: `GET`

门户首页
:param request:
:return:

**响应**:

**状态码 200**: Successful Response

Content-Type: `text/html`

---

### 代码生成

#### Gen List
**操作ID**: `gen_list_tool_gen_list_get`

**路径**: `/tool/gen/list`
**方法**: `GET`

查询代码生成列表

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableId | query |  | 否 | 编号 |
| tableName | query |  | 否 | 表名称 |
| tableComment | query |  | 否 | 表描述 |
| subTableName | query |  | 否 | 关联子表的表名 |
| subTableFkName | query |  | 否 | 子表关联的外键名 |
| className | query |  | 否 | 实体类名称 |
| tplCategory | query |  | 否 | 使用的模板（crud单表操作 tree树表操作） |
| tplWebType | query |  | 否 | 前端模板类型（element-ui模版 element-plus模版） |
| packageName | query |  | 否 | 生成包路径 |
| moduleName | query |  | 否 | 生成模块名 |
| businessName | query |  | 否 | 生成业务名 |
| functionName | query |  | 否 | 生成功能名 |
| functionAuthor | query |  | 否 | 生成功能作者 |
| genType | query |  | 否 | 生成代码方式（0zip压缩包 1自定义路径） |
| genPath | query |  | 否 | 生成路径（不填默认项目路径） |
| options | query |  | 否 | 其它生成选项 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| columns | query |  | 否 | 关联列 |
| params | query |  | 否 | 前端传递过来的表附加信息，转换成json字符串后放到options |
| parentMenuId | query |  | 否 | 解析出options里面的parentMenuId给前端用 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Gen Db List
**操作ID**: `gen_db_list_tool_gen_db_list_get`

**路径**: `/tool/gen/db/list`
**方法**: `GET`

查询数据库列表

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableId | query |  | 否 | 编号 |
| tableName | query |  | 否 | 表名称 |
| tableComment | query |  | 否 | 表描述 |
| subTableName | query |  | 否 | 关联子表的表名 |
| subTableFkName | query |  | 否 | 子表关联的外键名 |
| className | query |  | 否 | 实体类名称 |
| tplCategory | query |  | 否 | 使用的模板（crud单表操作 tree树表操作） |
| tplWebType | query |  | 否 | 前端模板类型（element-ui模版 element-plus模版） |
| packageName | query |  | 否 | 生成包路径 |
| moduleName | query |  | 否 | 生成模块名 |
| businessName | query |  | 否 | 生成业务名 |
| functionName | query |  | 否 | 生成功能名 |
| functionAuthor | query |  | 否 | 生成功能作者 |
| genType | query |  | 否 | 生成代码方式（0zip压缩包 1自定义路径） |
| genPath | query |  | 否 | 生成路径（不填默认项目路径） |
| options | query |  | 否 | 其它生成选项 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| columns | query |  | 否 | 关联列 |
| params | query |  | 否 | 前端传递过来的表附加信息，转换成json字符串后放到options |
| parentMenuId | query |  | 否 | 解析出options里面的parentMenuId给前端用 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Import Table
**操作ID**: `import_table_tool_gen_importTable_post`

**路径**: `/tool/gen/importTable`
**方法**: `POST`

导入表结构

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tables | query | string | 否 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Info
**操作ID**: `get_info_tool_gen_getById__tableId__get`

**路径**: `/tool/gen/getById/{tableId}`
**方法**: `GET`

查询表详细信息

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableId | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Table Info
**操作ID**: `get_table_info_tool_gen_tableInfo__tableName__get`

**路径**: `/tool/gen/tableInfo/{tableName}`
**方法**: `GET`

获取表详细信息

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableName | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Update Save
**操作ID**: `update_save_tool_gen_put`

**路径**: `/tool/gen`
**方法**: `PUT`

修改保存代码生成业务

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete
**操作ID**: `delete_tool_gen__tableIds__delete`

**路径**: `/tool/gen/{tableIds}`
**方法**: `DELETE`

删除代码生成

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableIds | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Preview
**操作ID**: `preview_tool_gen_preview__tableId__get`

**路径**: `/tool/gen/preview/{tableId}`
**方法**: `GET`

预览代码

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableId | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Sync Db
**操作ID**: `sync_db_tool_gen_synchDb__tableName__get`

**路径**: `/tool/gen/synchDb/{tableName}`
**方法**: `GET`

同步数据库

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableName | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Batch Generate Code
**操作ID**: `batch_generate_code_tool_gen_batchGenCode_get`

**路径**: `/tool/gen/batchGenCode`
**方法**: `GET`

批量生成代码

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tbIds | query |  | 是 | 当前页码 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Import Table
**操作ID**: `import_table_tool_gen_createTable_post`

**路径**: `/tool/gen/createTable`
**方法**: `POST`

创建表结构

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| sql | query | string | 否 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 导入数据

#### Upload Excel
**操作ID**: `upload_excel_import_uploadExcel_post`

**路径**: `/import/uploadExcel`
**方法**: `POST`

本地上传专用，用于临时解析，无需持久化存储的文件

**请求体**:

Content-Type: `multipart/form-data`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 测试业务

#### Get Car Driver List
**操作ID**: `get_car_driver_list_car_driver_list_get`

**路径**: `/car/driver/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| age | query |  | 否 | 年龄 |
| carType | query |  | 否 | 车辆类型 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| delFlag | query |  | 否 | 删除标志 |
| deptId | query |  | 否 | 部门id |
| driverYears | query |  | 否 | 驾龄 |
| id | query |  | 否 | id |
| image | query |  | 否 | 图片 |
| location | query |  | 否 | 所在位置 |
| name | query |  | 否 | 司机名称 |
| price | query |  | 否 | 价格 |
| updateTime | query |  | 否 | 更新时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Car Driver By Id
**操作ID**: `get_car_driver_by_id_car_driver_getById__carDriverId__get`

**路径**: `/car/driver/getById/{carDriverId}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| carDriverId | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add Car Driver
**操作ID**: `add_car_driver_car_driver_add_post`

**路径**: `/car/driver/add`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Update Car Driver
**操作ID**: `update_car_driver_car_driver_update_put`

**路径**: `/car/driver/update`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Del Car Driver
**操作ID**: `del_car_driver_car_driver_delete__carDriverIds__delete`

**路径**: `/car/driver/delete/{carDriverIds}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| carDriverIds | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export Car Driver
**操作ID**: `export_car_driver_car_driver_export_post`

**路径**: `/car/driver/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Import Data
**操作ID**: `import_data_car_driver_import_post`

**路径**: `/car/driver/import`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Student Info List
**操作ID**: `get_student_info_list_student_info_list_get`

**路径**: `/student/info/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| className | query |  | 否 | 班级 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| dateOfBirth | query |  | 否 | 出生日期 |
| delFlag | query |  | 否 | 删除标志 |
| deptId | query |  | 否 | 部门id |
| email | query |  | 否 | 电子邮箱 |
| gender | query |  | 否 | 性别 |
| id | query |  | 否 | ID |
| major | query |  | 否 | 专业 |
| name | query |  | 否 | 姓名 |
| phoneNumber | query |  | 否 | 联系电话 |
| updateTime | query |  | 否 | 更新时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Student Info By Id
**操作ID**: `get_student_info_by_id_student_info_getById__studentInfoId__get`

**路径**: `/student/info/getById/{studentInfoId}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| studentInfoId | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add Student Info
**操作ID**: `add_student_info_student_info_add_post`

**路径**: `/student/info/add`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Update Student Info
**操作ID**: `update_student_info_student_info_update_put`

**路径**: `/student/info/update`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Del Student Info
**操作ID**: `del_student_info_student_info_delete__studentInfoIds__delete`

**路径**: `/student/info/delete/{studentInfoIds}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| studentInfoIds | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export Student Info
**操作ID**: `export_student_info_student_info_export_post`

**路径**: `/student/info/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Import Student Info
**操作ID**: `import_student_info_student_info_import_post`

**路径**: `/student/info/import`
**方法**: `POST`

导入数据

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 登录模块

#### Login
**操作ID**: `login_login_post`

**路径**: `/login`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Login User Info
**操作ID**: `get_login_user_info_getInfo_get`

**路径**: `/getInfo`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Get Login User Routers
**操作ID**: `get_login_user_routers_getRouters_get`

**路径**: `/getRouters`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Register User
**操作ID**: `register_user_register_post`

**路径**: `/register`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Logout
**操作ID**: `logout_logout_post`

**路径**: `/logout`
**方法**: `POST`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### 用户登录注册
**操作ID**: `register_with_code_api_v1_wechat_auth_register_post`

**路径**: `/api/v1/wechat/auth/register`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 用户使用openid登录
**操作ID**: `register_with_code_api_v1_wechat_auth_login_post`

**路径**: `/api/v1/wechat/auth/login`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### 获取微信信息
**操作ID**: `get_wx_user_info_api_v1_wechat_user_info_get`

**路径**: `/api/v1/wechat/user/info`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

### 系统工具-代码生成

#### Gen List
**操作ID**: `gen_list_tool_gen_list_get`

**路径**: `/tool/gen/list`
**方法**: `GET`

查询代码生成列表

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableId | query |  | 否 | 编号 |
| tableName | query |  | 否 | 表名称 |
| tableComment | query |  | 否 | 表描述 |
| subTableName | query |  | 否 | 关联子表的表名 |
| subTableFkName | query |  | 否 | 子表关联的外键名 |
| className | query |  | 否 | 实体类名称 |
| tplCategory | query |  | 否 | 使用的模板（crud单表操作 tree树表操作） |
| tplWebType | query |  | 否 | 前端模板类型（element-ui模版 element-plus模版） |
| packageName | query |  | 否 | 生成包路径 |
| moduleName | query |  | 否 | 生成模块名 |
| businessName | query |  | 否 | 生成业务名 |
| functionName | query |  | 否 | 生成功能名 |
| functionAuthor | query |  | 否 | 生成功能作者 |
| genType | query |  | 否 | 生成代码方式（0zip压缩包 1自定义路径） |
| genPath | query |  | 否 | 生成路径（不填默认项目路径） |
| options | query |  | 否 | 其它生成选项 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| columns | query |  | 否 | 关联列 |
| params | query |  | 否 | 前端传递过来的表附加信息，转换成json字符串后放到options |
| parentMenuId | query |  | 否 | 解析出options里面的parentMenuId给前端用 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Gen Db List
**操作ID**: `gen_db_list_tool_gen_db_list_get`

**路径**: `/tool/gen/db/list`
**方法**: `GET`

查询数据库列表

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableId | query |  | 否 | 编号 |
| tableName | query |  | 否 | 表名称 |
| tableComment | query |  | 否 | 表描述 |
| subTableName | query |  | 否 | 关联子表的表名 |
| subTableFkName | query |  | 否 | 子表关联的外键名 |
| className | query |  | 否 | 实体类名称 |
| tplCategory | query |  | 否 | 使用的模板（crud单表操作 tree树表操作） |
| tplWebType | query |  | 否 | 前端模板类型（element-ui模版 element-plus模版） |
| packageName | query |  | 否 | 生成包路径 |
| moduleName | query |  | 否 | 生成模块名 |
| businessName | query |  | 否 | 生成业务名 |
| functionName | query |  | 否 | 生成功能名 |
| functionAuthor | query |  | 否 | 生成功能作者 |
| genType | query |  | 否 | 生成代码方式（0zip压缩包 1自定义路径） |
| genPath | query |  | 否 | 生成路径（不填默认项目路径） |
| options | query |  | 否 | 其它生成选项 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| columns | query |  | 否 | 关联列 |
| params | query |  | 否 | 前端传递过来的表附加信息，转换成json字符串后放到options |
| parentMenuId | query |  | 否 | 解析出options里面的parentMenuId给前端用 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Import Table
**操作ID**: `import_table_tool_gen_importTable_post`

**路径**: `/tool/gen/importTable`
**方法**: `POST`

导入表结构

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tables | query | string | 否 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Info
**操作ID**: `get_info_tool_gen_getById__tableId__get`

**路径**: `/tool/gen/getById/{tableId}`
**方法**: `GET`

查询表详细信息

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableId | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Table Info
**操作ID**: `get_table_info_tool_gen_tableInfo__tableName__get`

**路径**: `/tool/gen/tableInfo/{tableName}`
**方法**: `GET`

获取表详细信息

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableName | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Update Save
**操作ID**: `update_save_tool_gen_put`

**路径**: `/tool/gen`
**方法**: `PUT`

修改保存代码生成业务

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete
**操作ID**: `delete_tool_gen__tableIds__delete`

**路径**: `/tool/gen/{tableIds}`
**方法**: `DELETE`

删除代码生成

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableIds | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Preview
**操作ID**: `preview_tool_gen_preview__tableId__get`

**路径**: `/tool/gen/preview/{tableId}`
**方法**: `GET`

预览代码

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableId | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Sync Db
**操作ID**: `sync_db_tool_gen_synchDb__tableName__get`

**路径**: `/tool/gen/synchDb/{tableName}`
**方法**: `GET`

同步数据库

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableName | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Batch Generate Code
**操作ID**: `batch_generate_code_tool_gen_batchGenCode_get`

**路径**: `/tool/gen/batchGenCode`
**方法**: `GET`

批量生成代码

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tbIds | query |  | 是 | 当前页码 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Import Table
**操作ID**: `import_table_tool_gen_createTable_post`

**路径**: `/tool/gen/createTable`
**方法**: `POST`

创建表结构

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| sql | query | string | 否 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统工具-表单构建

#### Get Sys Form List
**操作ID**: `get_sys_form_list_sys_form_list_get`

**路径**: `/sys/form/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| content | query |  | 否 | 表单代码 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| delFlag | query |  | 否 | 删除标志 |
| deptId | query |  | 否 | 部门id |
| formConf | query |  | 否 | 表单配置 |
| formData | query |  | 否 | 表单内容 |
| generateConf | query |  | 否 | 生成配置 |
| drawingList | query |  | 否 | 字段列表 |
| id | query |  | 否 | id |
| name | query |  | 否 | 表单名称 |
| updateTime | query |  | 否 | 更新时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Sys Form By Id
**操作ID**: `get_sys_form_by_id_sys_form_getById__sysFormId__get`

**路径**: `/sys/form/getById/{sysFormId}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| sysFormId | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add Sys Form
**操作ID**: `add_sys_form_sys_form_add_post`

**路径**: `/sys/form/add`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Update Sys Form
**操作ID**: `update_sys_form_sys_form_update_put`

**路径**: `/sys/form/update`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Del Sys Form
**操作ID**: `del_sys_form_sys_form_delete__sysFormIds__delete`

**路径**: `/sys/form/delete/{sysFormIds}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| sysFormIds | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export Sys Form
**操作ID**: `export_sys_form_sys_form_export_post`

**路径**: `/sys/form/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Sys Form Data List
**操作ID**: `get_sys_form_data_list_sys_form_data_list_get`

**路径**: `/sys/form_data/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| delFlag | query |  | 否 | 删除标志 |
| deptId | query |  | 否 | 部门id |
| formData | query |  | 否 | 表单数据 |
| formId | query |  | 否 | 表单ID |
| formName | query |  | 否 | 表单名称 |
| id | query |  | 否 | id |
| updateTime | query |  | 否 | 更新时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Sys Form Data By Id
**操作ID**: `get_sys_form_data_by_id_sys_form_data_getById__sysFormDataId__get`

**路径**: `/sys/form_data/getById/{sysFormDataId}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| sysFormDataId | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add Sys Form Data
**操作ID**: `add_sys_form_data_sys_form_data_add_post`

**路径**: `/sys/form_data/add`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Update Sys Form Data
**操作ID**: `update_sys_form_data_sys_form_data_update_put`

**路径**: `/sys/form_data/update`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Del Sys Form Data
**操作ID**: `del_sys_form_data_sys_form_data_delete__sysFormDataIds__delete`

**路径**: `/sys/form_data/delete/{sysFormDataIds}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| sysFormDataIds | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export Sys Form Data
**操作ID**: `export_sys_form_data_sys_form_data_export_post`

**路径**: `/sys/form_data/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统监控-在线用户

#### Get Monitor Online List
**操作ID**: `get_monitor_online_list_monitor_online_list_get`

**路径**: `/monitor/online/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tokenId | query |  | 否 | 会话编号 |
| userName | query |  | 否 | 登录名称 |
| deptName | query |  | 否 | 所属部门 |
| ipaddr | query |  | 否 | 主机 |
| loginLocation | query |  | 否 | 登录地点 |
| browser | query |  | 否 | 浏览器类型 |
| os | query |  | 否 | 操作系统 |
| loginTime | query |  | 否 | 登录时间 |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete Monitor Online
**操作ID**: `delete_monitor_online_monitor_online__token_ids__delete`

**路径**: `/monitor/online/{token_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| token_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统监控-定时任务

#### Get System Job List
**操作ID**: `get_system_job_list_monitor_job_list_get`

**路径**: `/monitor/job/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| jobId | query |  | 否 | 任务ID |
| jobName | query |  | 否 | 任务名称 |
| jobGroup | query |  | 否 | 任务组名 |
| jobExecutor | query |  | 否 | 任务执行器 |
| invokeTarget | query |  | 否 | 调用目标字符串 |
| jobArgs | query |  | 否 | 位置参数 |
| jobKwargs | query |  | 否 | 关键字参数 |
| cronExpression | query |  | 否 | cron执行表达式 |
| misfirePolicy | query |  | 否 | 计划执行错误策略（1立即执行 2执行一次 3放弃执行） |
| concurrent | query |  | 否 | 是否并发执行（0允许 1禁止） |
| status | query |  | 否 | 状态（0正常 1暂停） |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注信息 |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System Job
**操作ID**: `edit_system_job_monitor_job_put`

**路径**: `/monitor/job`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System Job
**操作ID**: `add_system_job_monitor_job_post`

**路径**: `/monitor/job`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Change System Job Status
**操作ID**: `change_system_job_status_monitor_job_changeStatus_put`

**路径**: `/monitor/job/changeStatus`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Execute System Job
**操作ID**: `execute_system_job_monitor_job_run_put`

**路径**: `/monitor/job/run`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete System Job
**操作ID**: `delete_system_job_monitor_job__job_ids__delete`

**路径**: `/monitor/job/{job_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| job_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System Job
**操作ID**: `query_detail_system_job_monitor_job__job_id__get`

**路径**: `/monitor/job/{job_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| job_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export System Job List
**操作ID**: `export_system_job_list_monitor_job_export_post`

**路径**: `/monitor/job/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get System Job Log List
**操作ID**: `get_system_job_log_list_monitor_jobLog_list_get`

**路径**: `/monitor/jobLog/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| jobLogId | query |  | 否 | 任务日志ID |
| jobName | query |  | 否 | 任务名称 |
| jobGroup | query |  | 否 | 任务组名 |
| jobExecutor | query |  | 否 | 任务执行器 |
| invokeTarget | query |  | 否 | 调用目标字符串 |
| jobArgs | query |  | 否 | 位置参数 |
| jobKwargs | query |  | 否 | 关键字参数 |
| jobTrigger | query |  | 否 | 任务触发器 |
| jobMessage | query |  | 否 | 日志信息 |
| status | query |  | 否 | 执行状态（0正常 1失败） |
| exceptionInfo | query |  | 否 | 异常信息 |
| createTime | query |  | 否 | 创建时间 |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Clear System Job Log
**操作ID**: `clear_system_job_log_monitor_jobLog_clean_delete`

**路径**: `/monitor/jobLog/clean`
**方法**: `DELETE`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Delete System Job Log
**操作ID**: `delete_system_job_log_monitor_jobLog__job_log_ids__delete`

**路径**: `/monitor/jobLog/{job_log_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| job_log_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export System Job Log List
**操作ID**: `export_system_job_log_list_monitor_jobLog_export_post`

**路径**: `/monitor/jobLog/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统监控-缓存监控

#### Get Monitor Cache Info
**操作ID**: `get_monitor_cache_info_monitor_cache_get`

**路径**: `/monitor/cache`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Get Monitor Cache Name
**操作ID**: `get_monitor_cache_name_monitor_cache_getNames_get`

**路径**: `/monitor/cache/getNames`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

数组项模式:

---

#### Get Monitor Cache Key
**操作ID**: `get_monitor_cache_key_monitor_cache_getKeys__cache_name__get`

**路径**: `/monitor/cache/getKeys/{cache_name}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| cache_name | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

数组项模式:

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Monitor Cache Value
**操作ID**: `get_monitor_cache_value_monitor_cache_getValue__cache_name___cache_key__get`

**路径**: `/monitor/cache/getValue/{cache_name}/{cache_key}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| cache_name | path | string | 是 |  |
| cache_key | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Clear Monitor Cache Name
**操作ID**: `clear_monitor_cache_name_monitor_cache_clearCacheName__cache_name__delete`

**路径**: `/monitor/cache/clearCacheName/{cache_name}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| cache_name | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Clear Monitor Cache Key
**操作ID**: `clear_monitor_cache_key_monitor_cache_clearCacheKey__cache_key__delete`

**路径**: `/monitor/cache/clearCacheKey/{cache_key}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| cache_key | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Clear Monitor Cache All
**操作ID**: `clear_monitor_cache_all_monitor_cache_clearCacheAll_delete`

**路径**: `/monitor/cache/clearCacheAll`
**方法**: `DELETE`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

### 系统监控-菜单管理

#### Get Monitor Server Info
**操作ID**: `get_monitor_server_info_monitor_server_get`

**路径**: `/monitor/server`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

### 系统管理-参数管理

#### Get System Config List
**操作ID**: `get_system_config_list_system_config_list_get`

**路径**: `/system/config/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| configId | query |  | 否 | 参数主键 |
| configName | query |  | 否 | 参数名称 |
| configKey | query |  | 否 | 参数键名 |
| configValue | query |  | 否 | 参数键值 |
| configType | query |  | 否 | 系统内置（Y是 N否） |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System Config
**操作ID**: `edit_system_config_system_config_put`

**路径**: `/system/config`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System Config
**操作ID**: `add_system_config_system_config_post`

**路径**: `/system/config`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Refresh System Config
**操作ID**: `refresh_system_config_system_config_refreshCache_delete`

**路径**: `/system/config/refreshCache`
**方法**: `DELETE`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Delete System Config
**操作ID**: `delete_system_config_system_config__config_ids__delete`

**路径**: `/system/config/{config_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| config_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System Config
**操作ID**: `query_detail_system_config_system_config__config_id__get`

**路径**: `/system/config/{config_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| config_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query System Config
**操作ID**: `query_system_config_system_config_configKey__config_key__get`

**路径**: `/system/config/configKey/{config_key}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| config_key | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export System Config List
**操作ID**: `export_system_config_list_system_config_export_post`

**路径**: `/system/config/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统管理-字典管理

#### Get System Dict Type List
**操作ID**: `get_system_dict_type_list_system_dict_type_list_get`

**路径**: `/system/dict/type/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| dictId | query |  | 否 | 字典主键 |
| dictName | query |  | 否 | 字典名称 |
| dictType | query |  | 否 | 字典类型 |
| status | query |  | 否 | 状态（0正常 1停用） |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System Dict Type
**操作ID**: `edit_system_dict_type_system_dict_type_put`

**路径**: `/system/dict/type`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System Dict Type
**操作ID**: `add_system_dict_type_system_dict_type_post`

**路径**: `/system/dict/type`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Refresh System Dict
**操作ID**: `refresh_system_dict_system_dict_type_refreshCache_delete`

**路径**: `/system/dict/type/refreshCache`
**方法**: `DELETE`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Delete System Dict Type
**操作ID**: `delete_system_dict_type_system_dict_type__dict_ids__delete`

**路径**: `/system/dict/type/{dict_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| dict_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query System Dict Type Options
**操作ID**: `query_system_dict_type_options_system_dict_type_optionselect_get`

**路径**: `/system/dict/type/optionselect`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

数组项模式:

---

#### Query Detail System Dict Type
**操作ID**: `query_detail_system_dict_type_system_dict_type__dict_id__get`

**路径**: `/system/dict/type/{dict_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| dict_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export System Dict Type List
**操作ID**: `export_system_dict_type_list_system_dict_type_export_post`

**路径**: `/system/dict/type/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query System Dict Type Data
**操作ID**: `query_system_dict_type_data_system_dict_data_type__dict_type__get`

**路径**: `/system/dict/data/type/{dict_type}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| dict_type | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get System Dict Data List
**操作ID**: `get_system_dict_data_list_system_dict_data_list_get`

**路径**: `/system/dict/data/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| dictCode | query |  | 否 | 字典编码 |
| dictSort | query |  | 否 | 字典排序 |
| dictLabel | query |  | 否 | 字典标签 |
| dictValue | query |  | 否 | 字典键值 |
| dictType | query |  | 否 | 字典类型 |
| cssClass | query |  | 否 | 样式属性（其他样式扩展） |
| listClass | query |  | 否 | 表格回显样式 |
| isDefault | query |  | 否 | 是否默认（Y是 N否） |
| status | query |  | 否 | 状态（0正常 1停用） |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System Dict Data
**操作ID**: `edit_system_dict_data_system_dict_data_put`

**路径**: `/system/dict/data`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System Dict Data
**操作ID**: `add_system_dict_data_system_dict_data_post`

**路径**: `/system/dict/data`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete System Dict Data
**操作ID**: `delete_system_dict_data_system_dict_data__dict_codes__delete`

**路径**: `/system/dict/data/{dict_codes}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| dict_codes | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System Dict Data
**操作ID**: `query_detail_system_dict_data_system_dict_data__dict_code__get`

**路径**: `/system/dict/data/{dict_code}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| dict_code | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export System Dict Data List
**操作ID**: `export_system_dict_data_list_system_dict_data_export_post`

**路径**: `/system/dict/data/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统管理-岗位管理

#### Get System Post List
**操作ID**: `get_system_post_list_system_post_list_get`

**路径**: `/system/post/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| postId | query |  | 否 | 岗位ID |
| postCode | query |  | 否 | 岗位编码 |
| postName | query |  | 否 | 岗位名称 |
| postSort | query |  | 否 | 显示顺序 |
| status | query |  | 否 | 状态（0正常 1停用） |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System Post
**操作ID**: `edit_system_post_system_post_put`

**路径**: `/system/post`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System Post
**操作ID**: `add_system_post_system_post_post`

**路径**: `/system/post`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete System Post
**操作ID**: `delete_system_post_system_post__post_ids__delete`

**路径**: `/system/post/{post_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| post_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System Post
**操作ID**: `query_detail_system_post_system_post__post_id__get`

**路径**: `/system/post/{post_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| post_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export System Post List
**操作ID**: `export_system_post_list_system_post_export_post`

**路径**: `/system/post/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统管理-日志管理

#### Get System Operation Log List
**操作ID**: `get_system_operation_log_list_monitor_operlog_list_get`

**路径**: `/monitor/operlog/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| operId | query |  | 否 | 日志主键 |
| title | query |  | 否 | 模块标题 |
| businessType | query |  | 否 | 业务类型（0其它 1新增 2修改 3删除 4授权 5导出 6导入 7强退 8生成代码 9清空数据） |
| method | query |  | 否 | 方法名称 |
| requestMethod | query |  | 否 | 请求方式 |
| operatorType | query |  | 否 | 操作类别（0其它 1后台用户 2手机端用户） |
| operName | query |  | 否 | 操作人员 |
| deptName | query |  | 否 | 部门名称 |
| operUrl | query |  | 否 | 请求URL |
| operIp | query |  | 否 | 主机地址 |
| operLocation | query |  | 否 | 操作地点 |
| operParam | query |  | 否 | 请求参数 |
| jsonResult | query |  | 否 | 返回参数 |
| status | query |  | 否 | 操作状态（0正常 1异常） |
| errorMsg | query |  | 否 | 错误消息 |
| operTime | query |  | 否 | 操作时间 |
| costTime | query |  | 否 | 消耗时间 |
| orderByColumn | query |  | 否 | 排序的字段名称 |
| isAsc | query |  | 否 | 排序方式（ascending升序 descending降序） |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Clear System Operation Log
**操作ID**: `clear_system_operation_log_monitor_operlog_clean_delete`

**路径**: `/monitor/operlog/clean`
**方法**: `DELETE`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Delete System Operation Log
**操作ID**: `delete_system_operation_log_monitor_operlog__oper_ids__delete`

**路径**: `/monitor/operlog/{oper_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| oper_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export System Operation Log List
**操作ID**: `export_system_operation_log_list_monitor_operlog_export_post`

**路径**: `/monitor/operlog/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get System Login Log List
**操作ID**: `get_system_login_log_list_monitor_logininfor_list_get`

**路径**: `/monitor/logininfor/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| infoId | query |  | 否 | 访问ID |
| userName | query |  | 否 | 用户账号 |
| ipaddr | query |  | 否 | 登录IP地址 |
| loginLocation | query |  | 否 | 登录地点 |
| browser | query |  | 否 | 浏览器类型 |
| os | query |  | 否 | 操作系统 |
| status | query |  | 否 | 登录状态（0成功 1失败） |
| msg | query |  | 否 | 提示消息 |
| loginTime | query |  | 否 | 访问时间 |
| orderByColumn | query |  | 否 | 排序的字段名称 |
| isAsc | query |  | 否 | 排序方式（ascending升序 descending降序） |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Clear System Login Log
**操作ID**: `clear_system_login_log_monitor_logininfor_clean_delete`

**路径**: `/monitor/logininfor/clean`
**方法**: `DELETE`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Delete System Login Log
**操作ID**: `delete_system_login_log_monitor_logininfor__info_ids__delete`

**路径**: `/monitor/logininfor/{info_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| info_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Unlock System User
**操作ID**: `unlock_system_user_monitor_logininfor_unlock__user_name__get`

**路径**: `/monitor/logininfor/unlock/{user_name}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| user_name | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export System Login Log List
**操作ID**: `export_system_login_log_list_monitor_logininfor_export_post`

**路径**: `/monitor/logininfor/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统管理-用户管理

#### Get System Dept Tree
**操作ID**: `get_system_dept_tree_system_user_deptTree_get`

**路径**: `/system/user/deptTree`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Get System User List
**操作ID**: `get_system_user_list_system_user_list_get`

**路径**: `/system/user/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| userId | query |  | 否 | 用户ID |
| deptId | query |  | 否 | 部门ID |
| userName | query |  | 否 | 用户账号 |
| nickName | query |  | 否 | 用户昵称 |
| userType | query |  | 否 | 用户类型（00系统用户） |
| email | query |  | 否 | 用户邮箱 |
| phonenumber | query |  | 否 | 手机号码 |
| sex | query |  | 否 | 用户性别（0男 1女 2未知） |
| avatar | query |  | 否 | 头像地址 |
| password | query |  | 否 | 密码 |
| status | query |  | 否 | 帐号状态（0正常 1停用） |
| delFlag | query |  | 否 | 删除标志（0代表存在 2代表删除） |
| loginIp | query |  | 否 | 最后登录IP |
| loginDate | query |  | 否 | 最后登录时间 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| admin | query |  | 否 | 是否为admin |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System User
**操作ID**: `edit_system_user_system_user_put`

**路径**: `/system/user`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System User
**操作ID**: `add_system_user_system_user_post`

**路径**: `/system/user`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete System User
**操作ID**: `delete_system_user_system_user__user_ids__delete`

**路径**: `/system/user/{user_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| user_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Reset System User Pwd
**操作ID**: `reset_system_user_pwd_system_user_resetPwd_put`

**路径**: `/system/user/resetPwd`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Change System User Status
**操作ID**: `change_system_user_status_system_user_changeStatus_put`

**路径**: `/system/user/changeStatus`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System User Profile
**操作ID**: `query_detail_system_user_profile_system_user_profile_get`

**路径**: `/system/user/profile`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Change System User Profile Info
**操作ID**: `change_system_user_profile_info_system_user_profile_put`

**路径**: `/system/user/profile`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System User
**操作ID**: `query_detail_system_user_system_user__get`

**路径**: `/system/user/`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| user_id | query |  | 否 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System User
**操作ID**: `query_detail_system_user_system_user__user_id__get`

**路径**: `/system/user/{user_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| user_id | path |  | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Change System User Profile Avatar
**操作ID**: `change_system_user_profile_avatar_system_user_profile_avatar_post`

**路径**: `/system/user/profile/avatar`
**方法**: `POST`

**请求体**:

Content-Type: `multipart/form-data`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Reset System User Password
**操作ID**: `reset_system_user_password_system_user_profile_updatePwd_put`

**路径**: `/system/user/profile/updatePwd`
**方法**: `PUT`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| oldPassword | query |  | 否 | 旧密码 |
| newPassword | query |  | 否 | 新密码 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Batch Import System User
**操作ID**: `batch_import_system_user_system_user_importData_post`

**路径**: `/system/user/importData`
**方法**: `POST`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| updateSupport | query | boolean | 是 |  |

**请求体**:

Content-Type: `multipart/form-data`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export System User Template
**操作ID**: `export_system_user_template_system_user_importTemplate_post`

**路径**: `/system/user/importTemplate`
**方法**: `POST`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Export System User List
**操作ID**: `export_system_user_list_system_user_export_post`

**路径**: `/system/user/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get System Allocated Role List
**操作ID**: `get_system_allocated_role_list_system_user_authRole__user_id__get`

**路径**: `/system/user/authRole/{user_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| user_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Update System Role User
**操作ID**: `update_system_role_user_system_user_authRole_put`

**路径**: `/system/user/authRole`
**方法**: `PUT`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| userId | query | integer | 是 |  |
| roleIds | query | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统管理-菜单管理

#### Get System Menu Tree
**操作ID**: `get_system_menu_tree_system_menu_treeselect_get`

**路径**: `/system/menu/treeselect`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

#### Get System Role Menu Tree
**操作ID**: `get_system_role_menu_tree_system_menu_roleMenuTreeselect__role_id__get`

**路径**: `/system/menu/roleMenuTreeselect/{role_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| role_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get System Menu List
**操作ID**: `get_system_menu_list_system_menu_list_get`

**路径**: `/system/menu/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| menuId | query |  | 否 | 菜单ID |
| menuName | query |  | 否 | 菜单名称 |
| parentId | query |  | 否 | 父菜单ID |
| orderNum | query |  | 否 | 显示顺序 |
| path | query |  | 否 | 路由地址 |
| component | query |  | 否 | 组件路径 |
| query | query |  | 否 | 路由参数 |
| routeName | query |  | 否 | 路由名称 |
| isFrame | query |  | 否 | 是否为外链（0是 1否） |
| isCache | query |  | 否 | 是否缓存（0缓存 1不缓存） |
| menuType | query |  | 否 | 菜单类型（M目录 C菜单 F按钮） |
| visible | query |  | 否 | 菜单状态（0显示 1隐藏） |
| status | query |  | 否 | 菜单状态（0正常 1停用） |
| perms | query |  | 否 | 权限标识 |
| icon | query |  | 否 | 菜单图标 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

数组项模式:

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System Menu
**操作ID**: `edit_system_menu_system_menu_put`

**路径**: `/system/menu`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System Menu
**操作ID**: `add_system_menu_system_menu_post`

**路径**: `/system/menu`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete System Menu
**操作ID**: `delete_system_menu_system_menu__menu_ids__delete`

**路径**: `/system/menu/{menu_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| menu_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System Menu
**操作ID**: `query_detail_system_menu_system_menu__menu_id__get`

**路径**: `/system/menu/{menu_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| menu_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统管理-表格管理

#### Get Sys Table List
**操作ID**: `get_sys_table_list_sys_table_list_get`

**路径**: `/sys/table/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| align | query |  | 否 | 对其方式 |
| createTime | query |  | 否 | 创建时间 |
| delFlag | query |  | 否 | 删除标志 |
| fieldName | query |  | 否 | 字段名 |
| fixed | query |  | 否 | 固定表头 |
| id | query |  | 否 | ID |
| label | query |  | 否 | 字段标签 |
| labelTip | query |  | 否 | 字段标签解释 |
| prop | query |  | 否 | 驼峰属性 |
| show | query |  | 否 | 可见 |
| sortable | query |  | 否 | 可排序 |
| tableName | query |  | 否 | 表名 |
| tooltip | query |  | 否 | 超出隐藏 |
| updateBy | query |  | 否 | 更新者 |
| updateByName | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| width | query |  | 否 | 宽度 |
| sequence | query |  | 否 | 字段顺序 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Sys Table List
**操作ID**: `get_sys_table_list_sys_table_listAll_get`

**路径**: `/sys/table/listAll`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| align | query |  | 否 | 对其方式 |
| createTime | query |  | 否 | 创建时间 |
| delFlag | query |  | 否 | 删除标志 |
| fieldName | query |  | 否 | 字段名 |
| fixed | query |  | 否 | 固定表头 |
| id | query |  | 否 | ID |
| label | query |  | 否 | 字段标签 |
| labelTip | query |  | 否 | 字段标签解释 |
| prop | query |  | 否 | 驼峰属性 |
| show | query |  | 否 | 可见 |
| sortable | query |  | 否 | 可排序 |
| tableName | query |  | 否 | 表名 |
| tooltip | query |  | 否 | 超出隐藏 |
| updateBy | query |  | 否 | 更新者 |
| updateByName | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| width | query |  | 否 | 宽度 |
| sequence | query |  | 否 | 字段顺序 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Gen Db List
**操作ID**: `gen_db_list_sys_table_db_list_get`

**路径**: `/sys/table/db/list`
**方法**: `GET`

查询数据库列表

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tableName | query |  | 否 | 表名 |
| tableComment | query |  | 否 | 表描述 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get Sys Table By Id
**操作ID**: `get_sys_table_by_id_sys_table_getById__sysTableId__get`

**路径**: `/sys/table/getById/{sysTableId}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| sysTableId | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add Sys Table
**操作ID**: `add_sys_table_sys_table_add_post`

**路径**: `/sys/table/add`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Import Sys Table
**操作ID**: `import_sys_table_sys_table_import_post`

**路径**: `/sys/table/import`
**方法**: `POST`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| tables | query | string | 否 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Update Sys Table
**操作ID**: `update_sys_table_sys_table_update_put`

**路径**: `/sys/table/update`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Del Sys Table
**操作ID**: `del_sys_table_sys_table_delete__sysTableIds__delete`

**路径**: `/sys/table/delete/{sysTableIds}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| sysTableIds | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export Sys Table
**操作ID**: `export_sys_table_sys_table_export_post`

**路径**: `/sys/table/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Sys Table Column Sort
**操作ID**: `sys_table_column_sort_sys_table_column_sort_post`

**路径**: `/sys/table/column/sort`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统管理-角色管理

#### Get System Role Dept Tree
**操作ID**: `get_system_role_dept_tree_system_role_deptTree__role_id__get`

**路径**: `/system/role/deptTree/{role_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| role_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get System Role List
**操作ID**: `get_system_role_list_system_role_list_get`

**路径**: `/system/role/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| roleId | query |  | 否 | 角色ID |
| roleName | query |  | 否 | 角色名称 |
| roleKey | query |  | 否 | 角色权限字符串 |
| roleSort | query |  | 否 | 显示顺序 |
| dataScope | query |  | 否 | 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限 5：仅本人数据权限） |
| menuCheckStrictly | query |  | 否 | 菜单树选择项是否关联显示 |
| deptCheckStrictly | query |  | 否 | 部门树选择项是否关联显示 |
| status | query |  | 否 | 角色状态（0正常 1停用） |
| delFlag | query |  | 否 | 删除标志（0代表存在 2代表删除） |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| admin | query |  | 否 | 是否为admin |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System Role
**操作ID**: `edit_system_role_system_role_put`

**路径**: `/system/role`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System Role
**操作ID**: `add_system_role_system_role_post`

**路径**: `/system/role`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System Role Datascope
**操作ID**: `edit_system_role_datascope_system_role_dataScope_put`

**路径**: `/system/role/dataScope`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete System Role
**操作ID**: `delete_system_role_system_role__role_ids__delete`

**路径**: `/system/role/{role_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| role_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System Role
**操作ID**: `query_detail_system_role_system_role__role_id__get`

**路径**: `/system/role/{role_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| role_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Export System Role List
**操作ID**: `export_system_role_list_system_role_export_post`

**路径**: `/system/role/export`
**方法**: `POST`

**请求体**:

Content-Type: `application/x-www-form-urlencoded`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Reset System Role Status
**操作ID**: `reset_system_role_status_system_role_changeStatus_put`

**路径**: `/system/role/changeStatus`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get System Allocated User List
**操作ID**: `get_system_allocated_user_list_system_role_authUser_allocatedList_get`

**路径**: `/system/role/authUser/allocatedList`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| userId | query |  | 否 | 用户ID |
| deptId | query |  | 否 | 部门ID |
| userName | query |  | 否 | 用户账号 |
| nickName | query |  | 否 | 用户昵称 |
| userType | query |  | 否 | 用户类型（00系统用户） |
| email | query |  | 否 | 用户邮箱 |
| phonenumber | query |  | 否 | 手机号码 |
| sex | query |  | 否 | 用户性别（0男 1女 2未知） |
| avatar | query |  | 否 | 头像地址 |
| password | query |  | 否 | 密码 |
| status | query |  | 否 | 帐号状态（0正常 1停用） |
| delFlag | query |  | 否 | 删除标志（0代表存在 2代表删除） |
| loginIp | query |  | 否 | 最后登录IP |
| loginDate | query |  | 否 | 最后登录时间 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| admin | query |  | 否 | 是否为admin |
| roleId | query |  | 否 | 角色ID |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get System Unallocated User List
**操作ID**: `get_system_unallocated_user_list_system_role_authUser_unallocatedList_get`

**路径**: `/system/role/authUser/unallocatedList`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| userId | query |  | 否 | 用户ID |
| deptId | query |  | 否 | 部门ID |
| userName | query |  | 否 | 用户账号 |
| nickName | query |  | 否 | 用户昵称 |
| userType | query |  | 否 | 用户类型（00系统用户） |
| email | query |  | 否 | 用户邮箱 |
| phonenumber | query |  | 否 | 手机号码 |
| sex | query |  | 否 | 用户性别（0男 1女 2未知） |
| avatar | query |  | 否 | 头像地址 |
| password | query |  | 否 | 密码 |
| status | query |  | 否 | 帐号状态（0正常 1停用） |
| delFlag | query |  | 否 | 删除标志（0代表存在 2代表删除） |
| loginIp | query |  | 否 | 最后登录IP |
| loginDate | query |  | 否 | 最后登录时间 |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| admin | query |  | 否 | 是否为admin |
| roleId | query |  | 否 | 角色ID |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System Role User
**操作ID**: `add_system_role_user_system_role_authUser_selectAll_put`

**路径**: `/system/role/authUser/selectAll`
**方法**: `PUT`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| userId | query |  | 否 | 用户ID |
| userIds | query |  | 否 | 用户ID信息 |
| roleId | query |  | 否 | 角色ID |
| roleIds | query |  | 否 | 角色ID信息 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Cancel System Role User
**操作ID**: `cancel_system_role_user_system_role_authUser_cancel_put`

**路径**: `/system/role/authUser/cancel`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Batch Cancel System Role User
**操作ID**: `batch_cancel_system_role_user_system_role_authUser_cancelAll_put`

**路径**: `/system/role/authUser/cancelAll`
**方法**: `PUT`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| userId | query |  | 否 | 用户ID |
| userIds | query |  | 否 | 用户ID信息 |
| roleId | query |  | 否 | 角色ID |
| roleIds | query |  | 否 | 角色ID信息 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get System Role Table Tree
**操作ID**: `get_system_role_table_tree_system_role_roleTableTreeSelect__role_id__get`

**路径**: `/system/role/roleTableTreeSelect/{role_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| role_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统管理-通知公告管理

#### Get System Notice List
**操作ID**: `get_system_notice_list_system_notice_list_get`

**路径**: `/system/notice/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| noticeId | query |  | 否 | 公告ID |
| noticeTitle | query |  | 否 | 公告标题 |
| noticeType | query |  | 否 | 公告类型（1通知 2公告） |
| noticeContent | query |  | 否 | 公告内容 |
| status | query |  | 否 | 公告状态（0正常 1关闭） |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| remark | query |  | 否 | 备注 |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |
| pageNum | query | integer | 否 | 当前页码 |
| pageSize | query | integer | 否 | 每页记录数 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System Notice
**操作ID**: `edit_system_notice_system_notice_put`

**路径**: `/system/notice`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System Notice
**操作ID**: `add_system_notice_system_notice_post`

**路径**: `/system/notice`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete System Notice
**操作ID**: `delete_system_notice_system_notice__notice_ids__delete`

**路径**: `/system/notice/{notice_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| notice_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System Post
**操作ID**: `query_detail_system_post_system_notice__notice_id__get`

**路径**: `/system/notice/{notice_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| notice_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 系统管理-部门管理

#### Get System Dept Tree For Edit Option
**操作ID**: `get_system_dept_tree_for_edit_option_system_dept_list_exclude__dept_id__get`

**路径**: `/system/dept/list/exclude/{dept_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| dept_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

数组项模式:

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Get System Dept List
**操作ID**: `get_system_dept_list_system_dept_list_get`

**路径**: `/system/dept/list`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| deptId | query |  | 否 | 部门id |
| parentId | query |  | 否 | 父部门id |
| ancestors | query |  | 否 | 祖级列表 |
| deptName | query |  | 否 | 部门名称 |
| orderNum | query |  | 否 | 显示顺序 |
| leader | query |  | 否 | 负责人 |
| phone | query |  | 否 | 联系电话 |
| email | query |  | 否 | 邮箱 |
| status | query |  | 否 | 部门状态（0正常 1停用） |
| delFlag | query |  | 否 | 删除标志（0代表存在 2代表删除） |
| createBy | query |  | 否 | 创建者 |
| createTime | query |  | 否 | 创建时间 |
| updateBy | query |  | 否 | 更新者 |
| updateTime | query |  | 否 | 更新时间 |
| beginTime | query |  | 否 | 开始时间 |
| endTime | query |  | 否 | 结束时间 |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

数组项模式:

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Edit System Dept
**操作ID**: `edit_system_dept_system_dept_put`

**路径**: `/system/dept`
**方法**: `PUT`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Add System Dept
**操作ID**: `add_system_dept_system_dept_post`

**路径**: `/system/dept`
**方法**: `POST`

**请求体**:

Content-Type: `application/json`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Delete System Dept
**操作ID**: `delete_system_dept_system_dept__dept_ids__delete`

**路径**: `/system/dept/{dept_ids}`
**方法**: `DELETE`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| dept_ids | path | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Query Detail System Dept
**操作ID**: `query_detail_system_dept_system_dept__dept_id__get`

**路径**: `/system/dept/{dept_id}`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| dept_id | path | integer | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 通用模块

#### Common Upload
**操作ID**: `common_upload_common_upload_post`

**路径**: `/common/upload`
**方法**: `POST`

**请求体**:

Content-Type: `multipart/form-data`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Common Download
**操作ID**: `common_download_common_download_get`

**路径**: `/common/download`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| fileName | query | string | 是 |  |
| delete | query | boolean | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

#### Common Download Resource
**操作ID**: `common_download_resource_common_download_resource_get`

**路径**: `/common/download/resource`
**方法**: `GET`

**参数**:

| 名称 | 位置 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- | ---- |
| resource | query | string | 是 |  |

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

**状态码 422**: Validation Error

Content-Type: `application/json`

---

### 验证码模块

#### Get Captcha Image
**操作ID**: `get_captcha_image_captchaImage_get`

**路径**: `/captchaImage`
**方法**: `GET`

**响应**:

**状态码 200**: Successful Response

Content-Type: `application/json`

---

## 模型定义

### AddRoleModel

新增角色模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| roleId |  | 否 | 角色ID |
| roleName |  | 否 | 角色名称 |
| roleKey |  | 否 | 角色权限字符串 |
| roleSort |  | 否 | 显示顺序 |
| dataScope |  | 否 | 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限 5：仅本人数据权限） |
| menuCheckStrictly |  | 否 | 菜单树选择项是否关联显示 |
| deptCheckStrictly |  | 否 | 部门树选择项是否关联显示 |
| status |  | 否 | 角色状态（0正常 1停用） |
| delFlag |  | 否 | 删除标志（0代表存在 2代表删除） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| admin |  | 否 | 是否为admin |
| deptIds | array | 否 | 部门ID信息 |
| menuIds | array | 否 | 菜单ID信息 |
| type |  | 否 | 操作类型 |

### AddUserModel

新增用户模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| userId |  | 否 | 用户ID |
| deptId |  | 否 | 部门ID |
| userName |  | 否 | 用户账号 |
| nickName |  | 否 | 用户昵称 |
| userType |  | 否 | 用户类型（00系统用户） |
| email |  | 否 | 用户邮箱 |
| phonenumber |  | 否 | 手机号码 |
| sex |  | 否 | 用户性别（0男 1女 2未知） |
| avatar |  | 否 | 头像地址 |
| password |  | 否 | 密码 |
| status |  | 否 | 帐号状态（0正常 1停用） |
| delFlag |  | 否 | 删除标志（0代表存在 2代表删除） |
| loginIp |  | 否 | 最后登录IP |
| loginDate |  | 否 | 最后登录时间 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| admin |  | 否 | 是否为admin |
| roleIds |  | 否 | 角色ID信息 |
| postIds |  | 否 | 岗位ID信息 |
| type |  | 否 | 操作类型 |

### AppLoginModelResp

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| token | string | 是 | token信息 |
| expiresIn | string | 是 | 过期时间 |
| user |  | 是 | 用户信息 |
| wxUser |  | 是 | 微信用户信息 |

### Body_batch_import_system_user_system_user_importData_post

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| file | string | 是 |  |

### Body_change_system_user_profile_avatar_system_user_profile_avatar_post

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| avatarfile | string | 是 |  |

### Body_common_upload_common_upload_post

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| file | string | 是 |  |

### Body_login_login_post

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| grant_type | string | 否 |  |
| username | string | 是 |  |
| password | string | 是 |  |
| scope | string | 否 |  |
| client_id |  | 否 |  |
| client_secret |  | 否 |  |
| code |  | 否 |  |
| uuid |  | 否 |  |
| login_info |  | 否 |  |

### Body_upload_excel_import_uploadExcel_post

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| tableName | string | 是 |  |
| file | string | 是 |  |

### CacheInfoModel

缓存监控对象对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| cacheKey |  | 否 | 缓存键名 |
| cacheName |  | 否 | 缓存名称 |
| cacheValue |  | 否 | 缓存内容 |
| remark |  | 否 | 备注 |

### CacheMonitorModel

缓存监控信息对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| commandStats |  | 否 | 命令统计 |
| dbSize |  | 否 | Key数量 |
| info |  | 否 | Redis信息 |

### CarDriverModel

表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| age |  | 否 | 年龄 |
| carType |  | 否 | 车辆类型 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| delFlag |  | 否 | 删除标志 |
| deptId |  | 否 | 部门id |
| driverYears |  | 否 | 驾龄 |
| id |  | 否 | id |
| image |  | 否 | 图片 |
| location |  | 否 | 所在位置 |
| name |  | 否 | 司机名称 |
| price |  | 否 | 价格 |
| updateTime |  | 否 | 更新时间 |

### CarDriverPageModel

分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| age |  | 否 | 年龄 |
| carType |  | 否 | 车辆类型 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| delFlag |  | 否 | 删除标志 |
| deptId |  | 否 | 部门id |
| driverYears |  | 否 | 驾龄 |
| id |  | 否 | id |
| image |  | 否 | 图片 |
| location |  | 否 | 所在位置 |
| name |  | 否 | 司机名称 |
| price |  | 否 | 价格 |
| updateTime |  | 否 | 更新时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### ChatMessageRequest

聊天消息请求模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| content | string | 是 | 消息内容 |
| user_id | string | 否 | 用户标识 |
| streaming | boolean | 否 | 是否使用流式返回 |

### ChatRequest

聊天请求模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| app_id | integer | 是 | DIFY应用ID |
| query | string | 是 | 用户输入/提问内容 |
| conversation_id |  | 否 | 会话ID，为空则创建新会话 |
| user_id | string | 是 | 用户标识，由开发者定义规则 |
| streaming | boolean | 否 | 是否使用流式返回 |
| inputs |  | 否 | 允许传入App定义的各变量值 |
| files |  | 否 | 上传的文件列表 |

### ChatResponse

聊天响应模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| conversation_id |  | 否 | 会话ID |
| message_id |  | 否 | 消息ID |
| answer | string | 否 | 回复内容 |
| error | boolean | 否 | 是否出错 |
| message |  | 否 | 错误消息 |
| metadata |  | 否 | 元数据 |

### ChatTitleRequest

聊天标题请求模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| title | string | 是 | 新标题 |

### ConfigModel

参数配置表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| configId |  | 否 | 参数主键 |
| configName |  | 否 | 参数名称 |
| configKey |  | 否 | 参数键名 |
| configValue |  | 否 | 参数键值 |
| configType |  | 否 | 系统内置（Y是 N否） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |

### ConfigPageQueryModel

参数配置管理分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| configId |  | 否 | 参数主键 |
| configName |  | 否 | 参数名称 |
| configKey |  | 否 | 参数键名 |
| configValue |  | 否 | 参数键值 |
| configType |  | 否 | 系统内置（Y是 N否） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| beginTime |  | 否 | 开始时间 |
| endTime |  | 否 | 结束时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### CpuInfo

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| cpuNum |  | 否 | 核心数 |
| used |  | 否 | CPU用户使用率 |
| sys |  | 否 | CPU系统使用率 |
| free |  | 否 | CPU当前空闲率 |

### CreateChatRequest

创建聊天请求模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| app_id | integer | 是 | 应用ID |
| user_id | integer | 是 | 用户ID |
| title | string | 否 | 聊天标题 |

### CrudResponseModel

操作响应模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| is_success | boolean | 是 | 操作是否成功 |
| message | string | 是 | 响应信息 |
| result |  | 否 | 响应结果 |

### CrudUserRoleModel

新增、删除用户关联角色及角色关联用户模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| userId |  | 否 | 用户ID |
| userIds |  | 否 | 用户ID信息 |
| roleId |  | 否 | 角色ID |
| roleIds |  | 否 | 角色ID信息 |

### CurrentUserModel

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| permissions | array | 是 | 权限信息 |
| roles | array | 是 | 角色信息 |
| user |  | 是 | 用户信息 |

### DeptModel

部门表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| deptId |  | 否 | 部门id |
| parentId |  | 否 | 父部门id |
| ancestors |  | 否 | 祖级列表 |
| deptName |  | 否 | 部门名称 |
| orderNum |  | 否 | 显示顺序 |
| leader |  | 否 | 负责人 |
| phone |  | 否 | 联系电话 |
| email |  | 否 | 邮箱 |
| status |  | 否 | 部门状态（0正常 1停用） |
| delFlag |  | 否 | 删除标志（0代表存在 2代表删除） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |

### DictDataModel

字典数据表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| dictCode |  | 否 | 字典编码 |
| dictSort |  | 否 | 字典排序 |
| dictLabel |  | 否 | 字典标签 |
| dictValue |  | 否 | 字典键值 |
| dictType |  | 否 | 字典类型 |
| cssClass |  | 否 | 样式属性（其他样式扩展） |
| listClass |  | 否 | 表格回显样式 |
| isDefault |  | 否 | 是否默认（Y是 N否） |
| status |  | 否 | 状态（0正常 1停用） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |

### DictDataPageQueryModel

字典数据管理分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| dictCode |  | 否 | 字典编码 |
| dictSort |  | 否 | 字典排序 |
| dictLabel |  | 否 | 字典标签 |
| dictValue |  | 否 | 字典键值 |
| dictType |  | 否 | 字典类型 |
| cssClass |  | 否 | 样式属性（其他样式扩展） |
| listClass |  | 否 | 表格回显样式 |
| isDefault |  | 否 | 是否默认（Y是 N否） |
| status |  | 否 | 状态（0正常 1停用） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| beginTime |  | 否 | 开始时间 |
| endTime |  | 否 | 结束时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### DictTypeModel

字典类型表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| dictId |  | 否 | 字典主键 |
| dictName |  | 否 | 字典名称 |
| dictType |  | 否 | 字典类型 |
| status |  | 否 | 状态（0正常 1停用） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |

### DictTypePageQueryModel

字典类型管理分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| dictId |  | 否 | 字典主键 |
| dictName |  | 否 | 字典名称 |
| dictType |  | 否 | 字典类型 |
| status |  | 否 | 状态（0正常 1停用） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| beginTime |  | 否 | 开始时间 |
| endTime |  | 否 | 结束时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### EditJobModel

编辑定时任务模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| jobId |  | 否 | 任务ID |
| jobName |  | 否 | 任务名称 |
| jobGroup |  | 否 | 任务组名 |
| jobExecutor |  | 否 | 任务执行器 |
| invokeTarget |  | 否 | 调用目标字符串 |
| jobArgs |  | 否 | 位置参数 |
| jobKwargs |  | 否 | 关键字参数 |
| cronExpression |  | 否 | cron执行表达式 |
| misfirePolicy |  | 否 | 计划执行错误策略（1立即执行 2执行一次 3放弃执行） |
| concurrent |  | 否 | 是否并发执行（0允许 1禁止） |
| status |  | 否 | 状态（0正常 1暂停） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注信息 |
| type |  | 否 | 操作类型 |

### EditUserModel

编辑用户模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| userId |  | 否 | 用户ID |
| deptId |  | 否 | 部门ID |
| userName |  | 否 | 用户账号 |
| nickName |  | 否 | 用户昵称 |
| userType |  | 否 | 用户类型（00系统用户） |
| email |  | 否 | 用户邮箱 |
| phonenumber |  | 否 | 手机号码 |
| sex |  | 否 | 用户性别（0男 1女 2未知） |
| avatar |  | 否 | 头像地址 |
| password |  | 否 | 密码 |
| status |  | 否 | 帐号状态（0正常 1停用） |
| delFlag |  | 否 | 删除标志（0代表存在 2代表删除） |
| loginIp |  | 否 | 最后登录IP |
| loginDate |  | 否 | 最后登录时间 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| admin |  | 否 | 是否为admin |
| roleIds |  | 否 | 角色ID信息 |
| postIds |  | 否 | 岗位ID信息 |
| type |  | 否 | 操作类型 |
| role |  | 否 | 角色信息 |

### GenTableModel

表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| tableId |  | 否 | 编号 |
| tableName |  | 否 | 表名称 |
| tableComment |  | 否 | 表描述 |
| subTableName |  | 否 | 关联子表的表名 |
| subTableFkName |  | 否 | 子表关联的外键名 |
| className |  | 否 | 实体类名称 |
| tplCategory |  | 否 | 使用的模板（crud单表操作 tree树表操作） |
| tplWebType |  | 否 | 前端模板类型（element-ui模版 element-plus模版） |
| packageName |  | 否 | 生成包路径 |
| moduleName |  | 否 | 生成模块名 |
| businessName |  | 否 | 生成业务名 |
| functionName |  | 否 | 生成功能名 |
| functionAuthor |  | 否 | 生成功能作者 |
| genType |  | 否 | 生成代码方式（0zip压缩包 1自定义路径） |
| genPath |  | 否 | 生成路径（不填默认项目路径） |
| options |  | 否 | 其它生成选项 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| columns |  | 否 | 关联列 |
| params |  | 否 | 前端传递过来的表附加信息，转换成json字符串后放到options |
| parentMenuId |  | 否 | 解析出options里面的parentMenuId给前端用 |

### HTTPValidationError

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| detail | array of object | 否 |  |

### ImportFieldModel

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| baseColumn |  | 是 | 数据库字段名 |
| excelColumn |  | 否 | excel字段名 |
| defaultValue |  | 否 | 默认值 |
| isRequired |  | 是 | 是否必传 |
| selected |  | 是 | 是否勾选 |

### ImportModel

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| tableName |  | 是 | 表名 |
| filedInfo |  | 是 | 字段关联表 |
| fileName |  | 是 | 文件名 |

### JobLogPageQueryModel

定时任务日志管理分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| jobLogId |  | 否 | 任务日志ID |
| jobName |  | 否 | 任务名称 |
| jobGroup |  | 否 | 任务组名 |
| jobExecutor |  | 否 | 任务执行器 |
| invokeTarget |  | 否 | 调用目标字符串 |
| jobArgs |  | 否 | 位置参数 |
| jobKwargs |  | 否 | 关键字参数 |
| jobTrigger |  | 否 | 任务触发器 |
| jobMessage |  | 否 | 日志信息 |
| status |  | 否 | 执行状态（0正常 1失败） |
| exceptionInfo |  | 否 | 异常信息 |
| createTime |  | 否 | 创建时间 |
| beginTime |  | 否 | 开始时间 |
| endTime |  | 否 | 结束时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### JobModel

定时任务调度表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| jobId |  | 否 | 任务ID |
| jobName |  | 否 | 任务名称 |
| jobGroup |  | 否 | 任务组名 |
| jobExecutor |  | 否 | 任务执行器 |
| invokeTarget |  | 否 | 调用目标字符串 |
| jobArgs |  | 否 | 位置参数 |
| jobKwargs |  | 否 | 关键字参数 |
| cronExpression |  | 否 | cron执行表达式 |
| misfirePolicy |  | 否 | 计划执行错误策略（1立即执行 2执行一次 3放弃执行） |
| concurrent |  | 否 | 是否并发执行（0允许 1禁止） |
| status |  | 否 | 状态（0正常 1暂停） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注信息 |

### JobPageQueryModel

定时任务管理分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| jobId |  | 否 | 任务ID |
| jobName |  | 否 | 任务名称 |
| jobGroup |  | 否 | 任务组名 |
| jobExecutor |  | 否 | 任务执行器 |
| invokeTarget |  | 否 | 调用目标字符串 |
| jobArgs |  | 否 | 位置参数 |
| jobKwargs |  | 否 | 关键字参数 |
| cronExpression |  | 否 | cron执行表达式 |
| misfirePolicy |  | 否 | 计划执行错误策略（1立即执行 2执行一次 3放弃执行） |
| concurrent |  | 否 | 是否并发执行（0允许 1禁止） |
| status |  | 否 | 状态（0正常 1暂停） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注信息 |
| beginTime |  | 否 | 开始时间 |
| endTime |  | 否 | 结束时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### LoginLogPageQueryModel

登录日志管理分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| infoId |  | 否 | 访问ID |
| userName |  | 否 | 用户账号 |
| ipaddr |  | 否 | 登录IP地址 |
| loginLocation |  | 否 | 登录地点 |
| browser |  | 否 | 浏览器类型 |
| os |  | 否 | 操作系统 |
| status |  | 否 | 登录状态（0成功 1失败） |
| msg |  | 否 | 提示消息 |
| loginTime |  | 否 | 访问时间 |
| orderByColumn |  | 否 | 排序的字段名称 |
| isAsc |  | 否 | 排序方式（ascending升序 descending降序） |
| beginTime |  | 否 | 开始时间 |
| endTime |  | 否 | 结束时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### MemoryInfo

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| total |  | 否 | 内存总量 |
| used |  | 否 | 已用内存 |
| free |  | 否 | 剩余内存 |
| usage |  | 否 | 使用率 |

### MenuModel

菜单表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| menuId |  | 否 | 菜单ID |
| menuName |  | 否 | 菜单名称 |
| parentId |  | 否 | 父菜单ID |
| orderNum |  | 否 | 显示顺序 |
| path |  | 否 | 路由地址 |
| component |  | 否 | 组件路径 |
| query |  | 否 | 路由参数 |
| routeName |  | 否 | 路由名称 |
| isFrame |  | 否 | 是否为外链（0是 1否） |
| isCache |  | 否 | 是否缓存（0缓存 1不缓存） |
| menuType |  | 否 | 菜单类型（M目录 C菜单 F按钮） |
| visible |  | 否 | 菜单状态（0显示 1隐藏） |
| status |  | 否 | 菜单状态（0正常 1停用） |
| perms |  | 否 | 权限标识 |
| icon |  | 否 | 菜单图标 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |

### NoticeModel

通知公告表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| noticeId |  | 否 | 公告ID |
| noticeTitle |  | 否 | 公告标题 |
| noticeType |  | 否 | 公告类型（1通知 2公告） |
| noticeContent |  | 否 | 公告内容 |
| status |  | 否 | 公告状态（0正常 1关闭） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |

### OperLogPageQueryModel

操作日志管理分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| operId |  | 否 | 日志主键 |
| title |  | 否 | 模块标题 |
| businessType |  | 否 | 业务类型（0其它 1新增 2修改 3删除 4授权 5导出 6导入 7强退 8生成代码 9清空数据） |
| method |  | 否 | 方法名称 |
| requestMethod |  | 否 | 请求方式 |
| operatorType |  | 否 | 操作类别（0其它 1后台用户 2手机端用户） |
| operName |  | 否 | 操作人员 |
| deptName |  | 否 | 部门名称 |
| operUrl |  | 否 | 请求URL |
| operIp |  | 否 | 主机地址 |
| operLocation |  | 否 | 操作地点 |
| operParam |  | 否 | 请求参数 |
| jsonResult |  | 否 | 返回参数 |
| status |  | 否 | 操作状态（0正常 1异常） |
| errorMsg |  | 否 | 错误消息 |
| operTime |  | 否 | 操作时间 |
| costTime |  | 否 | 消耗时间 |
| orderByColumn |  | 否 | 排序的字段名称 |
| isAsc |  | 否 | 排序方式（ascending升序 descending降序） |
| beginTime |  | 否 | 开始时间 |
| endTime |  | 否 | 结束时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### PageResponseModel

列表分页查询返回模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| rows | array | 否 |  |
| pageNum |  | 否 |  |
| pageSize |  | 否 |  |
| total | integer | 是 |  |
| hasNext |  | 否 |  |

### PostModel

岗位信息表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| postId |  | 否 | 岗位ID |
| postCode |  | 否 | 岗位编码 |
| postName |  | 否 | 岗位名称 |
| postSort |  | 否 | 显示顺序 |
| status |  | 否 | 状态（0正常 1停用） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |

### PostPageQueryModel

岗位管理分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| postId |  | 否 | 岗位ID |
| postCode |  | 否 | 岗位编码 |
| postName |  | 否 | 岗位名称 |
| postSort |  | 否 | 显示顺序 |
| status |  | 否 | 状态（0正常 1停用） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| beginTime |  | 否 | 开始时间 |
| endTime |  | 否 | 结束时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### PyInfo

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| total |  | 否 | 内存总量 |
| used |  | 否 | 已用内存 |
| free |  | 否 | 剩余内存 |
| usage |  | 否 | 使用率 |
| name |  | 否 | Python名称 |
| version |  | 否 | Python版本 |
| startTime |  | 否 | 启动时间 |
| runTime |  | 否 | 运行时长 |
| home |  | 否 | 安装路径 |

### RoleModel

角色表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| roleId |  | 否 | 角色ID |
| roleName |  | 否 | 角色名称 |
| roleKey |  | 否 | 角色权限字符串 |
| roleSort |  | 否 | 显示顺序 |
| dataScope |  | 否 | 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限 5：仅本人数据权限） |
| menuCheckStrictly |  | 否 | 菜单树选择项是否关联显示 |
| deptCheckStrictly |  | 否 | 部门树选择项是否关联显示 |
| status |  | 否 | 角色状态（0正常 1停用） |
| delFlag |  | 否 | 删除标志（0代表存在 2代表删除） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| admin |  | 否 | 是否为admin |

### RolePageQueryModel

角色管理分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| roleId |  | 否 | 角色ID |
| roleName |  | 否 | 角色名称 |
| roleKey |  | 否 | 角色权限字符串 |
| roleSort |  | 否 | 显示顺序 |
| dataScope |  | 否 | 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限 5：仅本人数据权限） |
| menuCheckStrictly |  | 否 | 菜单树选择项是否关联显示 |
| deptCheckStrictly |  | 否 | 部门树选择项是否关联显示 |
| status |  | 否 | 角色状态（0正常 1停用） |
| delFlag |  | 否 | 删除标志（0代表存在 2代表删除） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| admin |  | 否 | 是否为admin |
| beginTime |  | 否 | 开始时间 |
| endTime |  | 否 | 结束时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### SelectedRoleModel

是否选择角色模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| roleId |  | 否 | 角色ID |
| roleName |  | 否 | 角色名称 |
| roleKey |  | 否 | 角色权限字符串 |
| roleSort |  | 否 | 显示顺序 |
| dataScope |  | 否 | 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限 5：仅本人数据权限） |
| menuCheckStrictly |  | 否 | 菜单树选择项是否关联显示 |
| deptCheckStrictly |  | 否 | 部门树选择项是否关联显示 |
| status |  | 否 | 角色状态（0正常 1停用） |
| delFlag |  | 否 | 删除标志（0代表存在 2代表删除） |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| admin |  | 否 | 是否为admin |
| flag |  | 否 | 选择标识 |

### ServerMonitorModel

服务监控对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| cpu |  | 是 | CPU相关信息 |
| py |  | 是 | Python相关信息 |
| mem |  | 是 | 內存相关信息 |
| sys |  | 是 | 服务器相关信息 |
| sysFiles |  | 是 | 磁盘相关信息 |

### StudentInfoModel

表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| className |  | 否 | 班级 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| dateOfBirth |  | 否 | 出生日期 |
| delFlag |  | 否 | 删除标志 |
| deptId |  | 否 | 部门id |
| email |  | 否 | 电子邮箱 |
| gender |  | 否 | 性别 |
| id |  | 否 | ID |
| major |  | 否 | 专业 |
| name |  | 否 | 姓名 |
| phoneNumber |  | 否 | 联系电话 |
| updateTime |  | 否 | 更新时间 |

### StudentInfoPageModel

分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| className |  | 否 | 班级 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| dateOfBirth |  | 否 | 出生日期 |
| delFlag |  | 否 | 删除标志 |
| deptId |  | 否 | 部门id |
| email |  | 否 | 电子邮箱 |
| gender |  | 否 | 性别 |
| id |  | 否 | ID |
| major |  | 否 | 专业 |
| name |  | 否 | 姓名 |
| phoneNumber |  | 否 | 联系电话 |
| updateTime |  | 否 | 更新时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### SysFiles

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| dirName |  | 否 | 盘符路径 |
| sysTypeName |  | 否 | 盘符类型 |
| typeName |  | 否 | 文件类型 |
| total |  | 否 | 总大小 |
| used |  | 否 | 已经使用量 |
| free |  | 否 | 剩余大小 |
| usage |  | 否 | 资源的使用率 |

### SysFormDataModel

表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| delFlag |  | 否 | 删除标志 |
| deptId |  | 否 | 部门id |
| formData |  | 否 | 表单数据 |
| formId |  | 否 | 表单ID |
| formName |  | 否 | 表单名称 |
| id |  | 否 | id |
| updateTime |  | 否 | 更新时间 |

### SysFormDataPageModel

分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| delFlag |  | 否 | 删除标志 |
| deptId |  | 否 | 部门id |
| formData |  | 否 | 表单数据 |
| formId |  | 否 | 表单ID |
| formName |  | 否 | 表单名称 |
| id |  | 否 | id |
| updateTime |  | 否 | 更新时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### SysFormModel

表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| content |  | 否 | 表单代码 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| delFlag |  | 否 | 删除标志 |
| deptId |  | 否 | 部门id |
| formConf |  | 否 | 表单配置 |
| formData |  | 否 | 表单内容 |
| generateConf |  | 否 | 生成配置 |
| drawingList |  | 否 | 字段列表 |
| id |  | 否 | id |
| name |  | 否 | 表单名称 |
| updateTime |  | 否 | 更新时间 |

### SysFormPageModel

分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| content |  | 否 | 表单代码 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| delFlag |  | 否 | 删除标志 |
| deptId |  | 否 | 部门id |
| formConf |  | 否 | 表单配置 |
| formData |  | 否 | 表单内容 |
| generateConf |  | 否 | 生成配置 |
| drawingList |  | 否 | 字段列表 |
| id |  | 否 | id |
| name |  | 否 | 表单名称 |
| updateTime |  | 否 | 更新时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### SysInfo

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| computerIp |  | 否 | 服务器IP |
| computerName |  | 否 | 服务器名称 |
| osArch |  | 否 | 系统架构 |
| osName |  | 否 | 操作系统 |
| userDir |  | 否 | 项目路径 |

### SysTableColumnIdsModel

列排序

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| ids |  | 是 |  |

### SysTableModel

表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| align |  | 否 | 对其方式 |
| createTime |  | 否 | 创建时间 |
| delFlag |  | 否 | 删除标志 |
| fieldName |  | 否 | 字段名 |
| fixed |  | 否 | 固定表头 |
| id |  | 否 | ID |
| label |  | 否 | 字段标签 |
| labelTip |  | 否 | 字段标签解释 |
| prop |  | 否 | 驼峰属性 |
| show |  | 否 | 可见 |
| sortable |  | 否 | 可排序 |
| tableName |  | 否 | 表名 |
| tooltip |  | 否 | 超出隐藏 |
| updateBy |  | 否 | 更新者 |
| updateByName |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| width |  | 否 | 宽度 |
| sequence |  | 否 | 字段顺序 |

### SysTablePageModel

分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| align |  | 否 | 对其方式 |
| createTime |  | 否 | 创建时间 |
| delFlag |  | 否 | 删除标志 |
| fieldName |  | 否 | 字段名 |
| fixed |  | 否 | 固定表头 |
| id |  | 否 | ID |
| label |  | 否 | 字段标签 |
| labelTip |  | 否 | 字段标签解释 |
| prop |  | 否 | 驼峰属性 |
| show |  | 否 | 可见 |
| sortable |  | 否 | 可排序 |
| tableName |  | 否 | 表名 |
| tooltip |  | 否 | 超出隐藏 |
| updateBy |  | 否 | 更新者 |
| updateByName |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| width |  | 否 | 宽度 |
| sequence |  | 否 | 字段顺序 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### Token

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| access_token | string | 是 | token信息 |
| token_type | string | 是 | token类型 |

### UserDetailModel

获取用户详情信息响应模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| data |  | 否 | 用户信息 |
| postIds |  | 否 | 岗位ID信息 |
| posts | array of object | 是 | 岗位信息 |
| roleIds |  | 否 | 角色ID信息 |
| roles | array of object | 是 | 角色信息 |

### UserInfoModel

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| userId |  | 否 | 用户ID |
| deptId |  | 否 | 部门ID |
| userName |  | 否 | 用户账号 |
| nickName |  | 否 | 用户昵称 |
| userType |  | 否 | 用户类型（00系统用户） |
| email |  | 否 | 用户邮箱 |
| phonenumber |  | 否 | 手机号码 |
| sex |  | 否 | 用户性别（0男 1女 2未知） |
| avatar |  | 否 | 头像地址 |
| password |  | 否 | 密码 |
| status |  | 否 | 帐号状态（0正常 1停用） |
| delFlag |  | 否 | 删除标志（0代表存在 2代表删除） |
| loginIp |  | 否 | 最后登录IP |
| loginDate |  | 否 | 最后登录时间 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| admin |  | 否 | 是否为admin |
| postIds |  | 否 | 岗位ID信息 |
| roleIds |  | 否 | 角色ID信息 |
| dept |  | 否 | 部门信息 |
| role |  | 否 | 角色信息 |

### UserModel

用户表对应pydantic模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| userId |  | 否 | 用户ID |
| deptId |  | 否 | 部门ID |
| userName |  | 否 | 用户账号 |
| nickName |  | 否 | 用户昵称 |
| userType |  | 否 | 用户类型（00系统用户） |
| email |  | 否 | 用户邮箱 |
| phonenumber |  | 否 | 手机号码 |
| sex |  | 否 | 用户性别（0男 1女 2未知） |
| avatar |  | 否 | 头像地址 |
| password |  | 否 | 密码 |
| status |  | 否 | 帐号状态（0正常 1停用） |
| delFlag |  | 否 | 删除标志（0代表存在 2代表删除） |
| loginIp |  | 否 | 最后登录IP |
| loginDate |  | 否 | 最后登录时间 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| admin |  | 否 | 是否为admin |

### UserPageQueryModel

用户管理分页查询模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| userId |  | 否 | 用户ID |
| deptId |  | 否 | 部门ID |
| userName |  | 否 | 用户账号 |
| nickName |  | 否 | 用户昵称 |
| userType |  | 否 | 用户类型（00系统用户） |
| email |  | 否 | 用户邮箱 |
| phonenumber |  | 否 | 手机号码 |
| sex |  | 否 | 用户性别（0男 1女 2未知） |
| avatar |  | 否 | 头像地址 |
| password |  | 否 | 密码 |
| status |  | 否 | 帐号状态（0正常 1停用） |
| delFlag |  | 否 | 删除标志（0代表存在 2代表删除） |
| loginIp |  | 否 | 最后登录IP |
| loginDate |  | 否 | 最后登录时间 |
| createBy |  | 否 | 创建者 |
| createTime |  | 否 | 创建时间 |
| updateBy |  | 否 | 更新者 |
| updateTime |  | 否 | 更新时间 |
| remark |  | 否 | 备注 |
| admin |  | 否 | 是否为admin |
| beginTime |  | 否 | 开始时间 |
| endTime |  | 否 | 结束时间 |
| pageNum | integer | 否 | 当前页码 |
| pageSize | integer | 否 | 每页记录数 |

### UserProfileModel

获取个人信息响应模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| data |  | 是 | 用户信息 |
| postGroup |  | 是 | 岗位信息 |
| roleGroup |  | 是 | 角色信息 |

### UserRegister

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| username | string | 是 | 用户名称 |
| password | string | 是 | 用户密码 |
| confirmPassword | string | 是 | 用户二次确认密码 |
| code |  | 否 | 验证码 |
| uuid |  | 否 | 会话编号 |

### UserRoleResponseModel

用户角色关联管理列表返回模型

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| roles | array of object | 否 | 角色信息 |
| user |  | 是 | 用户信息 |

### UserWechatModel

用户微信信息

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| userId |  | 否 | 性别 |
| city |  | 否 | 城市 |
| country |  | 否 | 国家 |
| headImgUrl |  | 否 | 微信头像 |
| nickname |  | 否 | 微信昵称 |
| openid |  | 否 | openid |
| unionId |  | 否 | union_id |
| userPhone |  | 否 | 手机号 |
| province |  | 否 | 省份 |
| sex |  | 否 | 性别 |

### ValidationError

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| loc | array of object | 是 |  |
| msg | string | 是 |  |
| type | string | 是 |  |

### WxMiniLoginCode

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| login_code |  | 是 | login_code |

### WxMiniPhoneNumberCode

| 字段 | 类型 | 必填 | 描述 |
| ---- | ---- | ---- | ---- |
| login_code |  | 是 | login_code |
| phone_num_code |  | 是 | phone_num_code |
