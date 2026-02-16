<template>
  <div class="inventory">
    <!-- 操作栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="handleIn">
        <el-icon><Bottom /></el-icon>
        入库
      </el-button>
      
      <el-button @click="handleOut">
        <el-icon><Top /></el-icon>
        出库
      </el-button>
      
      <el-button type="warning" @click="showAlerts">
        <el-icon><Warning /></el-icon>
        库存预警
      </el-button>
    </div>
    
    <!-- 库存列表 -->
    <el-table :data="inventoryList" v-loading="loading">
      <el-table-column prop="material_code" label="物料编码" width="120" />
      
      <el-table-column prop="material_name" label="物料名称" min-width="180" />
      
      <el-table-column prop="warehouse" label="仓库" width="120" />
      
      <el-table-column prop="location" label="库位" width="120" />
      
      <el-table-column prop="batch_no" label="批次号" width="150" />
      
      <el-table-column prop="quantity" label="数量" width="100">
        <template #default="{ row }">
          <span :class="{ 'stock-warning': row.quantity < row.min_stock }">
            {{ row.quantity }}
          </span>
        </template>
      </el-table-column>
      
      <el-table-column prop="qc_status" label="质检状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.qc_status === 'pass' ? 'success' : 'warning'">
            {{ getQcStatusText(row.qc_status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleViewLogs(row)">查看记录</el-button>
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
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const inventoryList = ref([
  {
    id: 1,
    material_code: 'AL-001',
    material_name: '4mm铝合金板',
    warehouse: '主仓库',
    location: 'A-01-01',
    batch_no: '20240115-001',
    quantity: 150,
    min_stock: 100,
    qc_status: 'pass'
  },
  {
    id: 2,
    material_code: 'AL-002',
    material_name: '铝合金型材',
    warehouse: '材料库',
    location: 'B-02-03',
    batch_no: '20240120-002',
    quantity: 80,
    min_stock: 500,
    qc_status: 'pass'
  }
])

const getQcStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '待检',
    pass: '合格',
    fail: '不合格',
    quarantine: '隔离'
  }
  return map[status] || status
}

const handleIn = () => {
  // TODO: 入库
}

const handleOut = () => {
  // TODO: 出库
}

const showAlerts = () => {
  // TODO: 显示库存预警
  ElMessage.info('库存预警功能')
}

const handleViewLogs = (row: any) => {
  // TODO: 查看库存记录
}
</script>

<style lang="scss" scoped>
.inventory {
  .toolbar {
    margin-bottom: 20px;
    display: flex;
    gap: 12px;
  }
  
  .stock-warning {
    color: #F56C6C;
    font-weight: bold;
  }
  
  .pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
  }
}
</style>
