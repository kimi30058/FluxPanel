cd ~/repos/FluxPanel/flux-backend
find module_ai/core/model_runtime -type f -name "*.py" -exec sed -i 's/from core.model_runtime/from module_ai.core.model_runtime/g' {} \;
find module_ai/core/model_runtime -type f -name "*.py" -exec sed -i 's/import core.model_runtime/import module_ai.core.model_runtime/g' {} \;
