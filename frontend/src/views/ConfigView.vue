<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Card, List, Input, Button, message, Empty, Tag } from 'ant-design-vue'
import { configApi, type ConfigFile } from '@/api/config'
import { SaveOutlined, FileTextOutlined } from '@ant-design/icons-vue'

const configs = ref<string[]>([])
const selectedConfig = ref<ConfigFile | null>(null)
const editingContent = ref('')
const loading = ref(false)
const saving = ref(false)

const configDescriptions: Record<string, string> = {
  CONFIG: '全局配置 (LLM、Proxy、Agent)',
  IDENTITY: 'Agent 身份定义',
  USER: '用户信息',
  SOUL: '人格模板',
  MEMORY: '长期记忆',
  AGENTS: '工作空间规则',
  HEARTBEAT: '心跳任务',
  BOOTSTRAP: '初始化引导',
}

const loadConfigs = async () => {
  loading.value = true
  try {
    const res = await configApi.list()
    configs.value = res.configs
  } catch (error) {
    message.error('加载配置列表失败')
  } finally {
    loading.value = false
  }
}

const selectConfig = async (name: string) => {
  try {
    const res = await configApi.get(name)
    selectedConfig.value = res
    editingContent.value = res.content
  } catch (error) {
    message.error('加载配置失败')
  }
}

const saveConfig = async () => {
  if (!selectedConfig.value) return

  saving.value = true
  try {
    await configApi.update(selectedConfig.value.name, editingContent.value)
    message.success('保存成功')
  } catch (error) {
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadConfigs()
})
</script>

<template>
  <div class="config-view">
    <div class="config-header">
      <h1>配置管理</h1>
      <p>管理 Agent 的配置文件和身份信息</p>
    </div>

    <div class="config-content">
      <!-- 配置列表 -->
      <div class="config-list">
        <Card :loading="loading" class="list-card">
          <template #title>
            <FileTextOutlined /> 配置文件
          </template>
          <List :data-source="configs" :locale="{ emptyText: '暂无配置文件' }">
            <template #renderItem="{ item }">
              <List.Item
                @click="selectConfig(item)"
                :class="['config-item', { active: selectedConfig?.name === item }]"
              >
                <div class="config-item-content">
                  <span class="config-name">{{ item }}</span>
                  <Tag color="error" v-if="configDescriptions[item]">
                    {{ configDescriptions[item] }}
                  </Tag>
                </div>
              </List.Item>
            </template>
          </List>
        </Card>
      </div>

      <!-- 编辑区域 -->
      <div class="config-editor">
        <Card v-if="selectedConfig" class="editor-card">
          <template #title>
            <span>{{ selectedConfig.name }}</span>
            <Tag color="green" style="margin-left: 8px">.md</Tag>
          </template>
          <template #extra>
            <Button
              type="primary"
              :loading="saving"
              @click="saveConfig"
            >
              <SaveOutlined /> 保存
            </Button>
          </template>
          <Input.TextArea
            v-model:value="editingContent"
            :auto-size="{ minRows: 18, maxRows: 30 }"
            class="editor-textarea"
          />
        </Card>

        <Card v-else class="empty-card">
          <Empty
            description="请从左侧选择一个配置文件"
            :image-style="{ height: '80px' }"
          />
        </Card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.config-view {
  min-height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 24px;
  box-sizing: border-box;
}

.config-header {
  flex-shrink: 0;
  margin-bottom: 24px;
}

.config-header h1 {
  margin: 0 0 8px;
  font-size: 24px;
  font-weight: 500;
}

.config-header p {
  margin: 0;
  color: #999;
}

.config-content {
  display: flex;
  gap: 24px;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.config-list {
  width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.list-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.list-card :deep(.ant-card-body) {
  flex: 1;
  padding: 0;
  overflow-y: auto;
}

.config-item {
  cursor: pointer;
  padding: 12px 16px;
  transition: all 0.2s;
  border-bottom: 1px solid #f0f0f0;
}

.config-item:hover {
  background-color: #f5f5f5;
}

.config-item.active {
  background-color: #fff1f0;
  border-left: 3px solid #ff4d4f;
}

.config-item-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.config-name {
  font-weight: 500;
}

.config-editor {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.editor-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.editor-card :deep(.ant-card-head) {
  flex-shrink: 0;
}

.editor-card :deep(.ant-card-body) {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.editor-textarea {
  flex: 1;
  width: 100%;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
  resize: none;
}

.empty-card {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
