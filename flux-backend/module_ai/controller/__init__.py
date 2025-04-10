
from fastapi import APIRouter
from module_ai.controller.provider_controller import router as provider_router
from module_ai.controller.model_controller import router as model_router
from module_ai.controller.assistant_controller import router as assistant_router
from module_ai.controller.topic_controller import router as topic_router
from module_ai.controller.message_controller import router as message_router
from module_ai.controller.knowledge_base_controller import router as knowledge_base_router
from module_ai.controller.knowledge_item_controller import router as knowledge_item_router

router = APIRouter()

router.include_router(provider_router)
router.include_router(model_router)
router.include_router(assistant_router)
router.include_router(topic_router)
router.include_router(message_router)
router.include_router(knowledge_base_router)
router.include_router(knowledge_item_router)
