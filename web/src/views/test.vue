<template>
  <div class="app-container">
    <!-- Chat Section -->
    <div class="chat-section">
      <div class="chat-header">
        <img src="./components/llama.png" alt="ChatGPT" class="avatar" />
        <span style="color: #1b1f23"> {{ llmService }}</span>
      </div>
      <div class="chat-history">
        <div v-for="(message, index) in messages" :key="index" :class="['message', messageClass(message.type)]">
          <div class="message-avatar" v-if="message.type === 'bot'">
            <img src="./components/llama.png" alt="Bot Avatar" class="avatar" />
          </div>
          <div class="message-bubble">
            <p>{{ message.text }}</p>
          </div>
          <div class="message-avatar" v-if="message.type === 'user'">
            <img src="./components/avatar.webp" alt="User Avatar" class="avatar" />
          </div>
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

    <!-- Player List Section -->
    <div class="player-list">
      <div class="player-list-header">
        <span>Players</span>
      </div>
      <div v-for="(player, index) in availablePlayers" :key="index" :class="['player-card', `gradient-${index % gradients.length}`]">
        <div class="player-info">
          <img src="./components/avatar.webp" alt="Player Avatar" class="player-avatar"  />
          <div>
            <h3 class="player-name">{{ player.nickName }}</h3>
            <p class="player-score">{{ player.team }}/{{ player.region}}</p>
          </div>
        </div>
        <v-bottom-sheet inset>
          <template v-slot:activator="{ props }">
            <div class="text-center">
              <v-btn
                  class="select-button"
                  v-bind="props"
                  text="Select"
                  @click="addPlayerToTeam(player)"
              ></v-btn>
            </div>
          </template>

          <v-sheet>
            <TeamDisplay :team="selectedTeam" @deletePlayer="deletePlayerFromTeam"/>
          </v-sheet>
        </v-bottom-sheet>
      </div>
    </div>


  </div>
</template>
<script>
import TeamDisplay from "@/views/components/TeamDisplay.vue";
import { Client } from "@gradio/client";
import global from "..//global.js";


export default {
  components: {
    TeamDisplay
  },
  computed: {
    display () {
      return this.$vuetify.display
    },
  },
  mounted() {
    console.log(1);

  },
  data() {
    return {
      llmService: global.LLM_SERVICE_TPYE,
      selectedTeam: [],
      inputMessage: '',
      messages: [
        { type: 'bot', text: 'Yeah, it would help in forming a team!' },
      ],
      availablePlayers: [
        {image: './components/avatar.webp',
          nickName: 'tabseN',
          realName: 'Johannes Wodarz',
          team: 'BIG',
          region: 'NA',
          teamImage: './download.png',
          age: 25,
          rating: 20.17,
          impact: 1.22,
          dpr: 0.66,
          adr: 85.1,
          kast: 71.3,
          kpr: 0.74},
        {image: '../assets/avatar.webp',
          nickName: 'wacsc',
          realName: 'acgwefwef',
          team: 'BIG',
          age: 25,
          region: 'NA',
          rating: 100.17,
          impact: 0.1,
          dpr: 0.66,
          adr: 85.1,
          kast: 0.1,
          kpr: 0.74},
        {image: 'avatar.webp',
          nickName: 'Tony',
          realName: 'Ren',
          team: 'T1',
          age: 25,
          region: 'NA',
          rating: 1.17,
          impact: 1.22,
          dpr: 0.66,
          adr: 85.1,
          kast: 71.3,
          kpr: 0.74},
        {image: 'avatar.webp',
          nickName: 'SuperGlue',
          realName: 'Ren',
          team: 'T1',
          age: 25,
          region: 'NA',
          rating: 1.17,
          impact: 3,
          dpr: 0.66,
          adr: 1001,
          kast: 71.3,
          kpr: 0.74},
        {image: 'avatar.webp',
          nickName: '12',
          realName: 'Ren',
          team: 'T1',
          age: 25,
          region: 'NA',
          rating: 1.17,
          impact: 2,
          dpr: 0.66,
          adr: 85.1,
          kast: 71.3,
          kpr: 0.74},
        // 更多选手数据
        {image: './avatar.webp',
          nickName: 'tabseN',
          realName: 'Johannes Wodarz',
          team: 'BIG',
          region: 'NA',
          teamImage: './download.png',
          age: 25,
          rating: 20.17,
          impact: 1.22,
          dpr: 0.66,
          adr: 85.1,
          kast: 71.3,
          kpr: 0.74},
      ],
      gradients: [
        'linear-gradient(90deg, #FF8A65, #FF7043)',
        'linear-gradient(90deg, #BA68C8, #AB47BC)',
        'linear-gradient(90deg, #4FC3F7, #29B6F6)',
        'linear-gradient(90deg, #81C784, #66BB6A)',
        'linear-gradient(90deg, #FFD54F, #FFCA28)',
        'linear-gradient(90deg, #E57373, #EF5350)',
      ],
    };
  },
  methods: {
    addPlayerToTeam(player) {
      if (this.selectedTeam.length < 6 && !this.selectedTeam.includes(player)) {
        this.selectedTeam.push(player);
      }
    },
    async sendMessage() {
      if (!this.inputMessage.trim()) return;
      this.messages.push({type: 'user', text: this.inputMessage});
      this.messages.push({type: 'bot', text: `Bot response to: "${this.inputMessage}"`});
      try {
        const app = await Client.connect(global.GRADIO_LOCAL_LINK);

        // 等待预测结果 因为有await，可能导致获取回复的速度较慢,可以根据运行的gradio app 来显示具体的api格式
        const result = await app.predict("/chat", [this.inputMessage]);

        const botResponse = result.data;
        this.messages.push({ type: 'bot', text: botResponse });

      } catch (error) {
        this.messages.push({ type: 'bot', text: 'Sorry, I could not process your question at the moment.' });
      }
      this.inputMessage = '';
    },
    messageClass(type) {
      return type === 'user' ? 'user-message justify-end' : 'bot-message justify-start';
    },
    deletePlayerFromTeam(player) {
      const index = this.selectedTeam.indexOf(player);
      if (index > -1) { // 如果找到了该元素
        this.selectedTeam.splice(index, 1); // 删除元素
      }
    }
  }
};
</script>

<style scoped>
/* 全局背景设置 */
.app-container {
  display: flex;
  justify-content: space-between;
  padding: 30px; /* 增加整体容器的内边距 */
  background-color: #f5f7fa;
  height: 100vh;
  width: 100vw;
}

/* 聊天区域样式 */
.chat-section {
  width: 65%; /* 调整聊天区的宽度 */
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: bold;
}

.chat-history {
  flex-grow: 1;
  overflow-y: auto;
  background-color: #eef2f5;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 10px; /* 增加底部间距 */
}

.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px; /* 增加消息间距 */
}

.user-message .message-bubble {
  background-color: #0065f4;
  border-radius: 15px 15px 0 15px;
  align-self: flex-end;
}

.bot-message .message-bubble {
  background-color: #ffffff;
  border-radius: 15px 15px 15px 0;
  color: black;
  align-self: flex-start;
}

.message-avatar{
  padding-left: 10px;
  padding-right: 10px;
}

.message-bubble {
  padding: 10px;
  max-width: 70%; /* 调整气泡的最大宽度 */
  font-size: 14px;
  line-height: 1.4;
}

.avatar {
  width: 35px; /* 调整头像大小 */
  height: 35px;
  border-radius: 50%;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input-box {
  flex-grow: 1;
  padding: 10px;
  border-radius: 20px;
  border: 1px solid #ddd;
  outline: none;
}

.send-button {
  background-color: #6c63ff;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-button:hover {
  background-color: #4c47d8;
}

/* 玩家列表样式 */
.player-list {
  width: 30%; /* 调整玩家列表的宽度 */
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  overflow-y: scroll;
}
.player-info {
  display: flex;
  gap: 10px;
  align-items: center; /* 垂直居中 */
  height: 100%; /* 需要的高度 */
  text-align: center; /* 文本居中 */
}

.player-list-header {
  color: black;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px; /* 增加底部间距 */
}

.player-card {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: space-between;
  padding: 10px;
  border-radius: 15px;
  background-color: #f0f0f0;
}


.player-avatar {
  width: 100px;
  height: 100px;
}

.player-name {
  font-family: 'Bebas Neue', Impact, sans-serif; /* 选择一个粗体且霸气的字体 */
  font-size: 24px;
  color: #070602;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.player-score {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 20px;
  color: #d4ac0d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.select-button {
  background-color: #6c63ff;
  color: white;
  border: none;
  border-radius: 15px;
  padding: 5px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.select-button:hover {
  background-color: #4c47d8;
}
</style>
