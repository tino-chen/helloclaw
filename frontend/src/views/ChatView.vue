<script setup lang="ts">
import { ref, watch } from 'vue'
import { Input, Button, message } from 'ant-design-vue'
import { SendOutlined, PlusOutlined } from '@ant-design/icons-vue'
import { useRouter, useRoute } from 'vue-router'
import { sessionApi } from '@/api/session'
import LobsterIcon from '@/assets/lobster.svg'

const router = useRouter()
const route = useRoute()
const inputMessage = ref('')
const messages = ref<Array<{ role: string; content: string }>>([])
const loading = ref(false)

// 监听 session 参数变化，清空消息
watch(
  () => route.query.session,
  () => {
    messages.value = []
    inputMessage.value = ''
  }
)

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return

  const userMessage = inputMessage.value
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  loading.value = true

  try {
    // TODO: 实现真实的聊天 API 调用
    messages.value.push({
      role: 'assistant',
      content: 'HelloClaw 后端尚未完全实现，请稍后再试。',
    })
  } catch (error) {
    message.error('发送消息失败')
  } finally {
    loading.value = false
  }
}

const createNewSession = async () => {
  try {
    const res = await sessionApi.create()
    message.success('新建会话成功')
    router.push({ name: 'chat', query: { session: res.session_id } })
  } catch (error) {
    message.error('新建会话失败')
  }
}
</script>

<template>
  <div class="chat-view">
    <!-- 消息区域 -->
    <div class="chat-messages">
      <template v-if="messages.length > 0">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message-item', msg.role]"
        >
          <div class="message-avatar">
            <img v-if="msg.role === 'assistant'" :src="LobsterIcon" alt="HelloClaw" />
            <div v-else class="user-avatar">你</div>
          </div>
          <div class="message-content">
            <div class="message-text">{{ msg.content }}</div>
          </div>
        </div>
      </template>

      <!-- 空状态 - 简洁 -->
      <div v-else class="empty-state">
        <img :src="LobsterIcon" alt="HelloClaw" class="empty-icon" />
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input-wrapper">
      <div class="chat-input">
        <Input.TextArea
          v-model:value="inputMessage"
          placeholder="输入消息..."
          :auto-size="{ minRows: 1, maxRows: 4 }"
          @press-enter="(e: KeyboardEvent) => { if (!e.shiftKey) { e.preventDefault(); sendMessage() } }"
        />
        <div class="input-actions">
          <Button
            type="primary"
            shape="circle"
            :loading="loading"
            :disabled="!inputMessage.trim()"
            @click="sendMessage"
          >
            <template #icon>
              <SendOutlined />
            </template>
          </Button>
          <Button
            shape="circle"
            @click="createNewSession"
          >
            <template #icon>
              <PlusOutlined />
            </template>
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  width: 100%;
  box-sizing: border-box;
  background-color: #f5f5f5;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

/* 消息样式 */
.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  max-width: 80%;
}

.message-item.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-item.assistant {
  align-self: flex-start;
}

.message-avatar {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-avatar img {
  width: 36px;
  height: 36px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--color-primary);
  color: #fff;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message-text {
  padding: 12px 16px;
  border-radius: 16px;
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  line-height: 1.5;
}

.message-item.user .message-text {
  background-color: var(--color-primary);
  color: #fff;
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-icon {
  width: 120px;
  height: 120px;
  opacity: 0.6;
}

/* 输入区域 */
.chat-input-wrapper {
  padding: 20px 24px 40px 24px;
  background-color: #fff;
  border-top: 1px solid #f0f0f0;
}

.chat-input {
  display: flex;
  gap: 12px;
  align-items: center;
  max-width: 800px;
  margin: 0 auto;
}

.chat-input .ant-input {
  flex: 1;
  border-radius: 20px;
  padding: 8px 16px;
}

.input-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>
