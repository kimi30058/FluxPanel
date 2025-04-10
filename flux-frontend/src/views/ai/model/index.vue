<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="模型名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入模型名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="提供商" prop="providerId">
        <el-select v-model="queryParams.providerId" placeholder="请选择提供商" clearable>
          <el-option
            v-for="item in providerOptions"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="模型分组" prop="group">
        <el-input
          v-model="queryParams.group"
          placeholder="请输入模型分组"
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
          v-hasPermi="['ai:model:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['ai:model:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['ai:model:remove']"
        >删除</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="modelList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="ID" align="center" prop="id" />
      <el-table-column label="模型名称" align="center" prop="name" />
      <el-table-column label="提供商" align="center" prop="providerName" />
      <el-table-column label="模型分组" align="center" prop="group" />
      <el-table-column label="模型类型" align="center">
        <template #default="scope">
          <el-tag v-for="type in scope.row.types" :key="type" style="margin-right: 5px">{{ type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button
            type="text"
            icon="Edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['ai:model:edit']"
          >修改</el-button>
          <el-button
            type="text"
            icon="Delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['ai:model:remove']"
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

    <!-- 添加或修改AI模型对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="modelForm" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="模型名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入模型名称" />
        </el-form-item>
        <el-form-item label="提供商" prop="providerId">
          <el-select v-model="form.providerId" placeholder="请选择提供商">
            <el-option
              v-for="item in providerOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="模型分组" prop="group">
          <el-input v-model="form.group" placeholder="请输入模型分组" />
        </el-form-item>
        <el-form-item label="模型描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入模型描述" />
        </el-form-item>
        <el-form-item label="模型类型" prop="types">
          <el-select v-model="form.types" multiple placeholder="请选择模型类型">
            <el-option label="文本" value="text" />
            <el-option label="视觉" value="vision" />
            <el-option label="嵌入" value="embedding" />
            <el-option label="函数调用" value="function" />
            <el-option label="语音" value="audio" />
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
import { listModel, getModel, delModel, addModel, updateModel } from "@/api/ai/model";
import { listProvider } from "@/api/ai/provider";

const { proxy } = getCurrentInstance();

const modelList = ref([]);
const providerOptions = ref([]);
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
    providerId: null,
    group: null
  },
  rules: {
    name: [{ required: true, message: "模型名称不能为空", trigger: "blur" }],
    providerId: [{ required: true, message: "提供商不能为空", trigger: "change" }],
    group: [{ required: true, message: "模型分组不能为空", trigger: "blur" }]
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询AI模型列表 */
function getList() {
  loading.value = true;
  listModel(queryParams.value).then(response => {
    modelList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 查询提供商下拉列表 */
function getProviderOptions() {
  listProvider().then(response => {
    providerOptions.value = response.rows;
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
    providerId: null,
    group: null,
    description: null,
    types: []
  };
  proxy.resetForm("modelForm");
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
  getProviderOptions();
  open.value = true;
  title.value = "添加AI模型";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  getProviderOptions();
  const modelId = row.id || ids.value[0];
  getModel(modelId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改AI模型";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["modelForm"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateModel(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addModel(form.value).then(response => {
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
  const modelIds = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除AI模型编号为"' + modelIds + '"的数据项?').then(function() {
    return delModel(modelIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

getList();
getProviderOptions();
</script>
