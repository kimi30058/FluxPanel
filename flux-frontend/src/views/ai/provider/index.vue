<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="提供商类型" prop="type">
        <el-input
          v-model="queryParams.type"
          placeholder="请输入提供商类型"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="提供商名称" prop="name">
        <el-input
          v-model="queryParams.name"
          placeholder="请输入提供商名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="是否启用" prop="enabled">
        <el-select v-model="queryParams.enabled" placeholder="请选择" clearable>
          <el-option
            v-for="dict in dict.type.sys_normal_disable"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
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
          v-hasPermi="['ai:provider:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['ai:provider:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['ai:provider:remove']"
        >删除</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="providerList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="ID" align="center" prop="id" />
      <el-table-column label="提供商类型" align="center" prop="type" />
      <el-table-column label="提供商名称" align="center" prop="name" />
      <el-table-column label="API主机地址" align="center" prop="apiHost" />
      <el-table-column label="API版本" align="center" prop="apiVersion" />
      <el-table-column label="是否启用" align="center" prop="enabled">
        <template #default="scope">
          <dict-tag :options="dict.type.sys_normal_disable" :value="scope.row.enabled" />
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button
            type="text"
            icon="Edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['ai:provider:edit']"
          >修改</el-button>
          <el-button
            type="text"
            icon="Delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['ai:provider:remove']"
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

    <!-- 添加或修改AI提供商对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="providerForm" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="提供商类型" prop="type">
          <el-input v-model="form.type" placeholder="请输入提供商类型" />
        </el-form-item>
        <el-form-item label="提供商名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入提供商名称" />
        </el-form-item>
        <el-form-item label="API密钥" prop="apiKey">
          <el-input v-model="form.apiKey" placeholder="请输入API密钥" />
        </el-form-item>
        <el-form-item label="API主机地址" prop="apiHost">
          <el-input v-model="form.apiHost" placeholder="请输入API主机地址" />
        </el-form-item>
        <el-form-item label="API版本" prop="apiVersion">
          <el-input v-model="form.apiVersion" placeholder="请输入API版本" />
        </el-form-item>
        <el-form-item label="是否启用" prop="enabled">
          <el-radio-group v-model="form.enabled">
            <el-radio
              v-for="dict in dict.type.sys_normal_disable"
              :key="dict.value"
              :label="dict.value"
            >{{dict.label}}</el-radio>
          </el-radio-group>
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
import { listProvider, getProvider, delProvider, addProvider, updateProvider } from "@/api/ai/provider";

const { proxy } = getCurrentInstance();
const { sys_normal_disable } = proxy.useDict("sys_normal_disable");

const providerList = ref([]);
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
    type: null,
    name: null,
    enabled: null
  },
  rules: {
    type: [{ required: true, message: "提供商类型不能为空", trigger: "blur" }],
    name: [{ required: true, message: "提供商名称不能为空", trigger: "blur" }],
    apiKey: [{ required: true, message: "API密钥不能为空", trigger: "blur" }],
    apiHost: [{ required: true, message: "API主机地址不能为空", trigger: "blur" }]
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询AI提供商列表 */
function getList() {
  loading.value = true;
  listProvider(queryParams.value).then(response => {
    providerList.value = response.rows;
    total.value = response.total;
    loading.value = false;
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
    type: null,
    name: null,
    apiKey: null,
    apiHost: null,
    apiVersion: null,
    enabled: true
  };
  proxy.resetForm("providerForm");
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
  open.value = true;
  title.value = "添加AI提供商";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const providerId = row.id || ids.value[0];
  getProvider(providerId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改AI提供商";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["providerForm"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateProvider(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addProvider(form.value).then(response => {
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
  const providerIds = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除AI提供商编号为"' + providerIds + '"的数据项?').then(function() {
    return delProvider(providerIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

getList();
</script>
