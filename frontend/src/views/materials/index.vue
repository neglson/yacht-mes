<template>
  <div class="materials">
    <!-- 操作栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新建物料
      </el-button>
      
      <el-button @click="handleImport">
        <el-icon><Upload /></el-icon>
        批量导入
      </el-button>
      
      <div class="filter-group">
        <el-select v-model="filter.category" placeholder="分类" clearable style="width: 150px">
          <el-option label="铝合金" value="aluminum" />
          <el-option label="焊接材料" value="welding" />
          <el-option label="电气" value="electrical" />
          <el-option label="涂料" value="paint" />
        </el-select>
        
        <el-input
          v-model="filter.keyword"
          placeholder="搜索物料名称/编码"
          style="width: 250px"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>
    
    <!-- 物料列表 -->
    <el-table :data="materialList" v-loading="loading">
      <el-table-column prop="code" label="物料编码" width="120" />
      
      <el-table-column prop="name" label="物料名称" min-width="180">
        <template #default="{ row }">
          <div class="material-name">
            <span class="name">{{ row.name }}</span>
            <el-tag v-if="row.brand" size="small" type="info">{{ row.brand }}</el-tag>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column prop="model" label="型号/规格" width="150" />
      
      <el-table-column prop="unit" label="单位" width="80" />
      
      <el-table-column prop="unit_cost" label="单价" width="100">
        <template #default="{ row }">
          ¥{{ row.unit_cost?.toFixed(2) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="supplier" label="供应商" width="150" />
      
      <el-table-column label="库存" width="120">
        <template #default="{ row }">
          <div class="stock-info">
            <span :class="{ 'stock-warning': row.stock < row.min_stock }">
              {{ row.stock || 0 }}
            </span>
            <span v-if="row.stock < row.min_stock" class="warning-icon">⚠️</span>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleView(row)">查看</el-button>
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="success" @click="handleStock(row)">库存</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[10, 20, 50, 100]"
      />
    </div>
    
    <!-- 库存管理对话框 -->
    <el-dialog v-model="stockDialogVisible" :title="`库存管理 - ${currentMaterial?.name}`" width="700px">
      <el-descriptions :column="2" border class="material-info">
        <el-descriptions-item label="物料编码">{{ currentMaterial?.code }}</el-descriptions-item>
        <el-descriptions-item label="型号">{{ currentMaterial?.model }}</el-descriptions-item>
        <el-descriptions-item label="当前库存">
          <span :class="{ 'stock-warning': currentStock < currentMaterial?.min_stock }">
            {{ currentStock }}
          </span>
        </el-descriptions-item>
        <el-descriptions-item label="安全库存">{{ currentMaterial?.min_stock }}</el-descriptions-item>
      </el-descriptions>
      
      <div class="stock-actions">
        <el-radio-group v-model="stockAction">
          <el-radio-button label="in">入库</el-radio-button>
          <el-radio-button label="out">出库</el-radio-button>
        </el-radio-group>
      </div>
      
      <el-form :model="stockForm" label-width="100px">
        <el-form-item label="数量">
          <el-input-number v-model="stockForm.quantity" :min="1" :precision="2" />
        </el-form-item>
        
        <el-form-item label="仓库">
          <el-select v-model="stockForm.warehouse" placeholder="选择仓库">
            <el-option label="主仓库" value="main" />
            <el-option label="材料库" value="material" />
            <el-option label="成品库" value="finished" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="库位">
          <el-input v-model="stockForm.location" placeholder="如：A-01-02" />
        </el-form-item>
        
        <el-form-item label="批次号">
          <el-input v-model="stockForm.batch_no" placeholder="可选" />
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input v-model="stockForm.remark" type="textarea" rows="2" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="stockDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitStock" :loading="submitting">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const filter = reactive({
  category: '',
  keyword: ''
})

const materialList = ref([
  {
    id: 1,
    code: 'AL-001',
    name: '4mm铝合金板',
    brand: 'CCS',
    model: '5083-H116',
    unit: '平米',
    unit_cost: 280,
    supplier: '中铝',
    stock: 150,
    min_stock: 100
  },
  {
    id: 2,
    code: 'AL-002',
    name: '铝合金型材',
    brand: 'CCS',
    model: '6061-T6',
    unit: '米',
    unit_cost: 45,
    supplier: '中铝',
    stock: 80,
    min_stock: 500
  },
  {
    id: 3,
    code: 'WELD-001',
    name: '铝合金焊丝',
    brand: 'ER5356',
    model: '1.2mm',
    unit: 'kg',
    unit_cost: 35,
    supplier: '大西洋',
    stock: 200,
    min_stock: 50
  }
])

const stockDialogVisible = ref(false)
const stockAction = ref('in')
const submitting = ref(false)
const currentMaterial = ref<any>(null)
const currentStock = ref(0)

const stockForm = reactive({
  quantity: 1,
  warehouse: 'main',
  location: '',
  batch_no: '',
  remark: ''
})

const handleCreate = () => {
  // TODO: 新建物料
}

const handleImport = () => {
  // TODO: 批量导入
}

const handleView = (row: any) => {
  // TODO: 查看物料详情
}

const handleEdit = (row: any) => {
  // TODO: 编辑物料
}

const handleStock = (row: any) => {
  currentMaterial.value = row
  currentStock.value = row.stock || 0
  stockAction.value = 'in'
  stockForm.quantity = 1
  stockForm.warehouse = 'main'
  stockForm.location = ''
  stockForm.batch_no = ''
  stockForm.remark = ''
  stockDialogVisible.value = true
}

const submitStock = async () => {
  submitting.value = true
  try {
    // TODO: 调用库存变更 API
    await new Promise(resolve => setTimeout(resolve, 500))
    
    if (stockAction.value === 'in') {
      currentMaterial.value.stock += stockForm.quantity
      ElMessage.success('入库成功')
    } else {
      currentMaterial.value.stock -= stockForm.quantity
      ElMessage.success('出库成功')
    }
    
    stockDialogVisible.value = false
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    submitting.value = false
  }
}
</script>

<style lang="scss" scoped>
.materials {
  .toolbar {
    display: flex;
    gap: 16px;
    margin-bottom: 20px;
    
    .filter-group {
      display: flex;
      gap: 12px;
      margin-left: auto;
    }
  }
  
  .material-name {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .name {
      font-weight: 500;
    }
  }
  
  .stock-info {
    display: flex;
    align-items: center;
    gap: 4px;
    
    .stock-warning {
      color: #F56C6C;
      font-weight: bold;
    }
    
    .warning-icon {
      font-size: 12px;
    }
  }
  
  .pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
  }
  
  .material-info {
    margin-bottom: 20px;
    
    .stock-warning {
      color: #F56C6C;
      font-weight: bold;
    }
  }
  
  .stock-actions {
    margin-bottom: 20px;
    text-align: center;
  }
}
</style>
