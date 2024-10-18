<template>
  <div class="chat-container">
    <v-card-title>Esport Chat</v-card-title>
    <div class="chat-history">
      <div v-for="(message, index) in messages" :key="index" :class="['message', messageClass(message.type)]">
        <div class="message-content">{{ message.text }}</div>
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
      return type === 'user' ? 'justify-end' : 'justify-start';
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  background-color: #2c2c2c;
  border-radius: 10px;
  padding: 20px;
}

.chat-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.chat-history {
  flex-grow: 1;
  overflow-y: auto;
  background-color: #333;
  padding: 10px;
  border-radius: 5px;
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.message-content {
  background-color: #555;
  padding: 10px;
  border-radius: 10px;
  color: white;
}

.chat-input {
  display: flex;
  margin-top: 20px;
}

.chat-input-box {
  flex-grow: 1;
  padding: 10px;
  border-radius: 5px;
  background-color: #555;
  color: white;
}

.send-button {
  background-color: #007bff;
  color: white;
  padding: 10px;
  margin-left: 10px;
  border-radius: 5px;
  cursor: pointer;
}
</style>
