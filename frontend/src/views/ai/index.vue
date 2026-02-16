<template>
  <div class="ai-assistant">
    <!-- 左侧功能菜单 -->
    <div class="sidebar">
      <div class="menu-header">
        <el-icon size="32" color="#409EFF"><Cpu /></el-icon>
        <span class="title">AI 助手</span>
      </div>
      
      <el-menu :default-active="activeMenu" @select="handleMenuSelect">
        <el-menu-item index="query">
          <el-icon><Search /></el-icon>
          <span>智能查询</span>
        </el-menu-item>
        
        <el-menu-item index="procurement">
          <el-icon><ShoppingCart /></el-icon>
          <span>采购建议</span>
        </el-menu-item>
        
        <el-menu-item index="report">
          <el-icon><Document /></el-icon>
          <span>日报生成</span>
        </el-menu-item>
        
        <el-menu-item index="knowledge">
          <el-icon><Reading /></el-icon>
          <span>工艺知识</span>
        </el-menu-item>
      </el-menu>
    </div>
    
    <!-- 右侧内容区 -->
    <div class="content">
      <!-- 智能查询 -->
      <template v-if="activeMenu === 'query'">
        <div class="chat-container">
          <div class="chat-header">
            <h3>💬 智能数据查询</h3>
            <p class="subtitle">用自然语言查询系统数据，如"查询本周延期的任务"</p>
          </div>
          
          <div class="chat-messages" ref="messageContainer">
            <div v-for="(msg, index) in queryMessages" :key="index" 
                 :class="['message', msg.role]">
              <div class="avatar">
                <el-avatar v-if="msg.role === 'user'" :size="36">
                  {{ userStore.userInfo?.real_name?.[0] || '我' }}
                </el-avatar>
                <el-avatar v-else :size="36" src="/ai-avatar.png">🤖</el-avatar>
              </div>
              
              <div class="bubble">
                <div class="text" v-html="formatMessage(msg.content)"></div>
                <div v-if="msg.sql" class="sql-box">
                  <pre><code>{{ msg.sql }}</code></pre>
                  <el-button type="primary" size="small" @click="executeSql(msg.sql)">执行查询</el-button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="chat-input">
            <el-input
              v-model="queryInput"
              type="textarea"
              :rows="2"
              placeholder="输入您的问题，如：查询铝合金班组本周的任务"
              @keyup.enter.ctrl="sendQuery"
            />
            <div class="input-actions">
              <span class="hint">Ctrl + Enter 发送</span>
              <el-button type="primary" @click="sendQuery" :loading="queryLoading">
                <el-icon><Promotion /></el-icon>
                发送
              </el-button>
            </div>
          </div>
        </div>
      </template>
      
      <!-- 采购建议 -->
      <template v-if="activeMenu === 'procurement'">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>🛒 AI 采购建议</span>
              <el-select v-model="selectedProject" placeholder="选择项目" style="width: 200px">
                <el-option v-for="p in projects" :key="p.id" :label="p.yacht_name" :value="p.id" />
              </el-select>
            </div>
          </template>
          
          <el-button type="primary" @click="getProcurementAdvice" :loading="procurementLoading">
            <el-icon><MagicStick /></el-icon>
            生成采购建议
          </el-button>
          
          <div v-if="procurementAdvice" class="advice-content">
            <pre>{{ procurementAdvice }}</pre>
          </div>
        </el-card>
      </template>
      
      <!-- 日报生成 -->
      <template v-if="activeMenu === 'report'">
        <el-card>
          <template #header>
            <span>📋 AI 日报生成</span>
          </template>
          
          <el-date-picker
            v-model="reportDate"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
          />
          
          <el-button 
            type="primary" 
            @click="generateReport" 
            :loading="reportLoading"
            style="margin-left: 12px"
          >
            <el-icon><DocumentChecked /></el-icon>
            生成日报
          </el-button>
          
          <div v-if="dailyReport" class="report-content">
            <div class="report-actions">
              <el-button type="primary" link @click="copyReport">
                <el-icon><CopyDocument /></el-icon>
                复制
              </el-button>
              
              <el-button type="primary" link @click="exportReport">
                <el-icon><Download /></el-icon>
                导出
              </el-button>
            </div>
            
            <pre>{{ dailyReport }}</pre>
          </div>
        </el-card>
      </template>
      
      <!-- 工艺知识 -->
      <template v-if="activeMenu === 'knowledge'">
        <div class="chat-container">
          <div class="chat-header">
            <h3>📚 工艺知识助手</h3>
            <p class="subtitle">询问焊接、涂装、检验等工艺规范</p>
          </div>
          
          <div class="chat-messages">
            <div v-for="(msg, index) in knowledgeMessages" :key="index" 
                 :class="['message', msg.role]">
              <div class="avatar">
                <el-avatar v-if="msg.role === 'user'" :size="36">
                  {{ userStore.userInfo?.real_name?.[0] || '我' }}
                </el-avatar>
                <el-avatar v-else :size="36">👨‍🔧</el-avatar>
              </div>
              
              <div class="bubble">
                <div class="text" v-html="formatMessage(msg.content)"></div>
              </div>
            </div>
          </div>
          
          <div class="chat-input">
            <el-input
              v-model="knowledgeInput"
              type="textarea"
              :rows="2"
              placeholder="输入您的问题，如：船体对接焊间隙标准是多少？"
              @keyup.enter.ctrl="sendKnowledgeQuery"
            />
            
            <div class="input-actions">
              <span class="hint">Ctrl + Enter 发送</span>
              <el-button type="primary" @click="sendKnowledgeQuery" :loading="knowledgeLoading">
                <el-icon><Promotion /></el-icon>
                提问
              </el-button>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const activeMenu = ref('query')

// 智能查询
const queryInput = ref('')
const queryLoading = ref(false)
const queryMessages = ref<any[]>([
  {
    role: 'assistant',
    content: '您好！我是您的数据查询助手。您可以问我：\n- "查询本周延期的任务"\n- "库存低于安全线的物料有哪些"\n- "铝合金班组进行中的任务"'
  }
])

// 采购建议
const selectedProject = ref(null)
const procurementLoading = ref(false)
const procurementAdvice = ref('')
const projects = ref([
  { id: 1, yacht_name: '海鹰号' },
  { id: 2, yacht_name: '蓝鲸号' }
])

// 日报
const reportDate = ref('')
const reportLoading = ref(false)
const dailyReport = ref('')

// 工艺知识
const knowledgeInput = ref('')
const knowledgeLoading = ref(false)
const knowledgeMessages = ref<any[]>([
  {
    role: 'assistant',
    content: '您好！我是工艺知识助手，熟悉铝合金游艇建造的各类规范。请随时提问！'
  }
])

const handleMenuSelect = (index: string) => {
  activeMenu.value = index
}

const formatMessage = (content: string) => {
  return content.replace(/\n/g, '<br>')
}

const sendQuery = async () => {
  if (!queryInput.value.trim()) return
  
  const question = queryInput.value
  queryMessages.value.push({ role: 'user', content: question })
  queryInput.value = ''
  queryLoading.value = true
  
  try {
    // TODO: 调用 AI 查询 API
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    queryMessages.value.push({
      role: 'assistant',
      content: '根据您的查询，我为您生成了以下 SQL 语句：',
      sql: 'SELECT * FROM tasks WHERE status = \'delayed\' AND plan_start >= \'2024-02-01\''
    })
  } catch (error: any) {
    ElMessage.error(error.message || '查询失败')
  } finally {
    queryLoading.value = false
  }
}

const executeSql = (sql: string) => {
  ElMessage.success('执行查询: ' + sql.substring(0, 50) + '...')
}

const getProcurementAdvice = async () => {
  if (!selectedProject.value) {
    ElMessage.warning('请先选择项目')
    return
  }
  
  procurementLoading.value = true
  try {
    // TODO: 调用 API
    await new Promise(resolve => setTimeout(resolve, 2000))
    procurementAdvice.value = `## 采购建议报告

### 1. 紧急采购清单
- 4mm铝合金板 5083-H116：预计3天内用完，建议立即采购200平米
- 铝合金焊丝 ER5356：库存不足，建议采购500kg

### 2. 供应商比价建议
- 中铝：价格适中，质量稳定，推荐
- 西南铝：价格略低，交货期较长

### 3. 库存优化建议
- 铝合金型材库存积压，建议暂停采购
- 建议与供应商协商分批交货`
  } catch (error: any) {
    ElMessage.error(error.message || '获取建议失败')
  } finally {
    procurementLoading.value = false
  }
}

const generateReport = async () => {
  reportLoading.value = true
  try {
    // TODO: 调用 API
    await new Promise(resolve => setTimeout(resolve, 2000))
    dailyReport.value = `## 生产日报 (${reportDate.value || '今日'})

### 一、今日完成任务
1. 飞桥结构设计审核 - 设计部张三
2. 船体放样验收 - 生产部李四

### 二、进行中任务
1. 船体结构制作 (65%) - 预计4月30日完成
2. 电气系统设计 (80%) - 预计2月20日完成

### 三、延期任务
1. 外板矫正 - 延期5天，原因：材料延迟到货

### 四、明日计划
1. 继续船体结构制作
2. 开始电气系统布线

### 五、风险提示
- 铝合金板材库存不足，可能影响后续进度`
  } catch (error: any) {
    ElMessage.error(error.message || '生成失败')
  } finally {
    reportLoading.value = false
  }
}

const copyReport = () => {
  navigator.clipboard.writeText(dailyReport.value)
  ElMessage.success('已复制到剪贴板')
}

const exportReport = () => {
  ElMessage.success('导出功能开发中')
}

const sendKnowledgeQuery = async () => {
  if (!knowledgeInput.value.trim()) return
  
  const question = knowledgeInput.value
  knowledgeMessages.value.push({ role: 'user', content: question })
  knowledgeInput.value = ''
  knowledgeLoading.value = true
  
  try {
    // TODO: 调用 API
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    knowledgeMessages.value.push({
      role: 'assistant',
      content: `根据《铝合金船体建造规范》CCS 要求：

**船体对接焊间隙标准：**

1. **根部间隙**：3-5mm
2. **钝边高度**：1-2mm
3. **角度**：60°±5°

**注意事项：**
- 焊接前需清理坡口及两侧20mm范围内的氧化膜
- 环境温度低于5℃时需预热
- 焊后需进行外观检查和渗透检测

建议参考具体项目的焊接工艺评定报告(WPQR)。`
    })
  } catch (error: any) {
    ElMessage.error(error.message || '查询失败')
  } finally {
    knowledgeLoading.value = false
  }
}
</script>

<style lang="scss" scoped>
.ai-assistant {
  display: flex;
  height: calc(100vh - 100px);
  
  .sidebar {
    width: 220px;
    background: #fff;
    border-right: 1px solid #e8e8e8;
    
    .menu-header {
      padding: 20px;
      display: flex;
      align-items: center;
      gap: 12px;
      border-bottom: 1px solid #e8e8e8;
      
      .title {
        font-size: 18px;
        font-weight: 600;
      }
    }
    
    .el-menu {
      border-right: none;
    }
  }
  
  .content {
    flex: 1;
    padding: 20px;
    overflow: auto;
    
    .chat-container {
      display: flex;
      flex-direction: column;
      height: 100%;
      background: #fff;
      border-radius: 8px;
      
      .chat-header {
        padding: 20px;
        border-bottom: 1px solid #e8e8e8;
        
        h3 {
          margin: 0 0 8px;
        }
        
        .subtitle {
          color: #666;
          margin: 0;
        }
      }
      
      .chat-messages {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        
        .message {
          display: flex;
          gap: 12px;
          margin-bottom: 20px;
          
          &.user {
            flex-direction: row-reverse;
            
            .bubble {
              background: #409EFF;
              color: #fff;
            }
          }
          
          .bubble {
            max-width: 70%;
            padding: 12px 16px;
            background: #f5f5f5;
            border-radius: 12px;
            
            .sql-box {
              margin-top: 12px;
              padding: 12px;
              background: #1e1e1e;
              border-radius: 8px;
              
              pre {
                margin: 0 0 12px;
                color: #d4d4d4;
                overflow-x: auto;
              }
            }
          }
        }
      }
      
      .chat-input {
        padding: 20px;
        border-top: 1px solid #e8e8e8;
        
        .input-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-top: 12px;
          
          .hint {
            color: #999;
            font-size: 12px;
          }
        }
      }
    }
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .advice-content,
    .report-content {
      margin-top: 20px;
      padding: 20px;
      background: #f8f9fa;
      border-radius: 8px;
      
      pre {
        margin: 0;
        white-space: pre-wrap;
        line-height: 1.8;
      }
    }
    
    .report-actions {
      margin-bottom: 16px;
    }
  }
}
</style>
