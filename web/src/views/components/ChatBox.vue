<template>
  <div>
    <v-card-title>Esport Chat</v-card-title>
    <div class="chat-history">
      <div v-for="(message, index) in messages" :key="index" :class="['message', messageClass(message.type)]">

        <div class="message-content"> {{ message.text }}</div>
      </div>
    </div>
    <div class="chat-input">
      <input
          v-model="inputMessage"
          @keydown.enter="sendMessage"
          placeholder="Type your message..."
          class="chat-input-box"
      />
      <button @click="sendMessage" class="send-button">Send</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    messages: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      inputMessage: ''
    };
  },
  methods: {
    sendMessage() {
      if (!this.inputMessage.trim()) return;
      this.$emit('sendMessage', this.inputMessage);
      this.inputMessage = '';
    },
    messageClass(type) {
      return type === 'user' ? 'user-message justify-end' : 'bot-message justify-start';
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  background: rgba(30, 30, 30, 0.85); /* 半透明深色背景 */
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); /* 阴影效果 */
  max-width: 600px;
  margin: 0 auto;
  height: 70vh;
}

.chat-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  color: white;
}

.chat-history {
  flex-grow: 1;
  overflow-y: auto;
  background-color: rgba(50, 50, 50, 0.8); /* 半透明背景 */
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.user-message .message-content {
  background-color: #4a90e2; /* 用户消息气泡颜色 */
  align-self: flex-end;
  border-top-right-radius: 0; /* 定制圆角 */
}

.bot-message .message-content {
  background-color: #333; /* AI消息气泡颜色 */
  align-self: flex-start;
  border-top-left-radius: 0; /* 定制圆角 */
}

.message-content {
  padding: 10px;
  border-radius: 15px;
  color: white;
  max-width: 75%;
  word-wrap: break-word;
  animation: fadeIn 0.3s ease-in-out; /* 消息淡入动画 */
}

.chat-input {
  display: flex;
  margin-top: 10px;
}

.chat-input-box {
  flex-grow: 1;
  padding: 10px;
  border-radius: 5px;
  background-color: rgba(80, 80, 80, 0.9);
  color: white;
  border: none;
  outline: none;
}

.send-button {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  margin-left: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.send-button:hover {
  background-color: #0056b3; /* 悬停时按钮颜色变化 */
}

@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(5px); }
  100% { opacity: 1; transform: translateY(0); }
}
</style>
