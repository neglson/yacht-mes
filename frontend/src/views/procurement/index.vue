<template>
  <div class="procurement">
    <!-- 操作栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新建采购申请
      </el-button>
      
      <div class="filter-group">
        <el-select v-model="filter.status" placeholder="状态" clearable style="width: 120px">
          <el-option label="待审批" value="pending_approval" />
          <el-option label="已审批" value="approved" />
          <el-option label="已下单" value="ordered" />
          <el-option label="已到货" value="delivered" />
        </el-select>
        
        <el-input
          v-model="filter.keyword"
          placeholder="搜索采购单号/物料"
          style="width: 250px"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>
    
    <!-- 采购列表 -->
    <el-table :data="procurementList" v-loading="loading">
      <el-table-column prop="order_no" label="采购单号" width="150" />
      
      <el-table-column prop="material_name" label="物料名称" min-width="180" />
      
      <el-table-column prop="quantity" label="数量" width="100">
        <template #default="{ row }">
          {{ row.quantity }} {{ row.unit }}
        </template>
      </el-table-column>
      
      <el-table-column prop="total_price" label="总价" width="120">
        <template #default="{ row }">
          ¥{{ row.total_price?.toFixed(2) }}
        </template>
      </el-table-column>
      
      <el-table-column prop="supplier" label="供应商" width="150" />
      
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="delivery_date" label="交货日期" width="120" />
      
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending_approval'" link type="success" @click="handleApprove(row)">审批</el-button>
          <el-button link type="primary" @click="handleView(row)">查看</el-button>
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
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
  status: '',
  keyword: ''
})

const procurementList = ref([
  {
    id: 1,
    order_no: 'PO-2024-001',
    material_name: '4mm铝合金板',
    quantity: 200,
    unit: '平米',
    total_price: 56000,
    supplier: '中铝',
    status: 'delivered',
    delivery_date: '2024-01-20'
  },
  {
    id: 2,
    order_no: 'PO-2024-002',
    material_name: '铝合金焊丝',
    quantity: 500,
    unit: 'kg',
    total_price: 17500,
    supplier: '大西洋',
    status: 'pending_approval',
    delivery_date: '2024-02-15'
  }
])

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    draft: 'info',
    pending_approval: 'warning',
    approved: 'success',
    ordered: 'primary',
    delivered: 'success',
    cancelled: 'info'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    draft: '草稿',
    pending_approval: '待审批',
    approved: '已审批',
    ordered: '已下单',
    delivered: '已到货',
    cancelled: '已取消'
  }
  return map[status] || status
}

const handleCreate = () => {
  // TODO: 新建采购申请
}

const handleApprove = (row: any) => {
  // TODO: 审批
  row.status = 'approved'
  ElMessage.success('审批通过')
}

const handleView = (row: any) => {
  // TODO: 查看详情
}

const handleEdit = (row: any) => {
  // TODO: 编辑
}
</script>

<style lang="scss" scoped>
.procurement {
  .toolbar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    
    .filter-group {
      display: flex;
      gap: 12px;
    }
  }
  
  .pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
  }
}
</style>
