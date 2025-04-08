export interface ChatMessage {
  id: string | number;
  role: 'user' | 'assistant' | 'system';
  content: string;
  content_type?: 'text' | 'image' | 'file';
  file_name?: string;
  created_at?: string;
  updated_at?: string;
  status?: 'pending' | 'processing' | 'completed' | 'failed';
  tokens?: number;
  error_message?: string;
  metadata?: Record<string, any>;
  feedback?: {
    rating: 'like' | 'dislike' | null;
  };
}

export interface ChatSession {
  id: string;
  title: string;
  description?: string;
  chat_type?: 'normal' | 'ai';
  system_prompt?: string;
  config?: Record<string, any>;
  ai_application_id?: number;
  ai_application?: AIApplication;
  user_id?: number;
  lastTime?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ChatRequest {
  chat_id: number;
  content: string;
  content_type?: string;
  file_name?: string;
}

export interface ChatResponse {
  id: number;
  content: string;
  role: string;
  status?: string;
  created_at: string;
}

export interface AIApplication {
  id: number;
  name: string;
  description?: string;
  icon?: string;
  icon_bg_color?: string;
  type: string;
  system_prompt?: string;
  tags?: string[];
  max_context_turns: number;
  max_tokens: number;
  preserve_system_prompt: boolean;
  is_enabled: boolean;
  id_traditional_provider?: number;
  id_dify_app?: number;
  id_coze_app?: number;
  traditional_provider?: TraditionalProvider;
  dify_app?: DifyApplication;
  coze_app?: CozeApplication;
  created_at?: string;
  updated_at?: string;
}

export interface TraditionalProvider {
  id: number;
  name: string;
  provider: string;
  api_key: string;
  base_url?: string;
  available_models?: string[];
  config?: Record<string, any>;
  is_active: boolean;
}

export interface DifyApplication {
  id: number;
  api_key: string;
  app_id: string;
  api_base?: string;
  conversation_mode?: string;
  response_mode?: string;
  is_active: boolean;
}

export interface CozeApplication {
  id: number;
  api_key: string;
  workflow_id?: string;
  agent_id?: string;
  config?: Record<string, any>;
  is_active: boolean;
}
