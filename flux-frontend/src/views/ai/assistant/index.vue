<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="助手名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入助手名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="助手类型" prop="type">
        <el-input
          v-model="queryParams.type"
          placeholder="请输入助手类型"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['ai:assistant:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['ai:assistant:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['ai:assistant:remove']"
        >删除</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="assistantList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="ID" align="center" prop="id" />
      <el-table-column label="助手名称" align="center" prop="name" />
      <el-table-column label="助手类型" align="center" prop="type" />
      <el-table-column label="表情图标" align="center" prop="emoji" />
      <el-table-column label="助手描述" align="center" prop="description" :show-overflow-tooltip="true" />
      <el-table-column label="网络搜索" align="center" prop="enableWebSearch">
        <template #default="scope">
          <el-tag :type="scope.row.enableWebSearch ? 'success' : 'info'">
            {{ scope.row.enableWebSearch ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="图像生成" align="center" prop="enableGenerateImage">
        <template #default="scope">
          <el-tag :type="scope.row.enableGenerateImage ? 'success' : 'info'">
            {{ scope.row.enableGenerateImage ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button
            type="text"
            icon="Edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['ai:assistant:edit']"
          >修改</el-button>
          <el-button
            type="text"
            icon="Delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['ai:assistant:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改AI助手对话框 -->
    <el-dialog :title="title" v-model="open" width="700px" append-to-body>
      <el-form ref="assistantForm" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="助手名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入助手名称" />
        </el-form-item>
        <el-form-item label="助手类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择助手类型">
            <el-option label="通用" value="general" />
            <el-option label="编程" value="coding" />
            <el-option label="写作" value="writing" />
            <el-option label="翻译" value="translation" />
            <el-option label="数据分析" value="data_analysis" />
          </el-select>
        </el-form-item>
        <el-form-item label="表情图标" prop="emoji">
          <el-input v-model="form.emoji" placeholder="请输入表情图标" />
        </el-form-item>
        <el-form-item label="助手描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入助手描述" />
        </el-form-item>
        <el-form-item label="助手提示词" prop="prompt">
          <el-input v-model="form.prompt" type="textarea" :rows="5" placeholder="请输入助手提示词" />
        </el-form-item>
        <el-form-item label="模型" prop="modelId">
          <el-select v-model="form.modelId" placeholder="请选择模型">
            <el-option
              v-for="item in modelOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="默认模型" prop="defaultModelId">
          <el-select v-model="form.defaultModelId" placeholder="请选择默认模型">
            <el-option
              v-for="item in modelOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="网络搜索" prop="enableWebSearch">
          <el-switch v-model="form.enableWebSearch" />
        </el-form-item>
        <el-form-item label="图像生成" prop="enableGenerateImage">
          <el-switch v-model="form.enableGenerateImage" />
        </el-form-item>
        <el-form-item label="知识库" prop="knowledgeBases">
          <el-select v-model="form.knowledgeBases" multiple placeholder="请选择知识库">
            <el-option
              v-for="item in knowledgeBaseOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { listAssistant, getAssistant, delAssistant, addAssistant, updateAssistant } from "@/api/ai/assistant";
import { listModel } from "@/api/ai/model";
import { listKnowledgeBase } from "@/api/ai/knowledge-base";

const { proxy } = getCurrentInstance();

const assistantList = ref([]);
const modelOptions = ref([]);
const knowledgeBaseOptions = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    name: null,
    type: null
  },
  rules: {
    name: [{ required: true, message: "助手名称不能为空", trigger: "blur" }],
    type: [{ required: true, message: "助手类型不能为空", trigger: "change" }],
    prompt: [{ required: true, message: "助手提示词不能为空", trigger: "blur" }]
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询AI助手列表 */
function getList() {
  loading.value = true;
  listAssistant(queryParams.value).then(response => {
    assistantList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 查询模型下拉列表 */
function getModelOptions() {
  listModel().then(response => {
    modelOptions.value = response.rows;
  });
}

/** 查询知识库下拉列表 */
function getKnowledgeBaseOptions() {
  listKnowledgeBase().then(response => {
    knowledgeBaseOptions.value = response.rows;
  });
}

/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}

/** 表单重置 */
function reset() {
  form.value = {
    id: null,
    name: null,
    type: null,
    emoji: null,
    description: null,
    prompt: null,
    modelId: null,
    defaultModelId: null,
    enableWebSearch: false,
    enableGenerateImage: false,
    knowledgeBases: []
  };
  proxy.resetForm("assistantForm");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryForm");
  handleQuery();
}

/** 多选框选中数据 */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id);
  single.value = selection.length !== 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  getModelOptions();
  getKnowledgeBaseOptions();
  open.value = true;
  title.value = "添加AI助手";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  getModelOptions();
  getKnowledgeBaseOptions();
  const assistantId = row.id || ids.value[0];
  getAssistant(assistantId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改AI助手";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["assistantForm"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateAssistant(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addAssistant(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const assistantIds = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除AI助手编号为"' + assistantIds + '"的数据项?').then(function() {
    return delAssistant(assistantIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

getList();
</script>
