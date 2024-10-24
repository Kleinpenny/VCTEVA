<template>
  <div class="app-container">
    <!-- Chat Section -->
    <div class="chat-section">
      <div class="chat-header">
        <img src="./components/llama.png" alt="ChatGPT" class="avatar" />
        <span style="color: #1b1f23"> {{ llmService }}</span>
      </div>
      <div class="chat-history" style="display: flex; flex-direction: column; align-items: flex-start;">
        <div v-for="(message, index) in messages" :key="index" :class="['message', messageClass(message.type)]" style="display: flex; align-items: flex-start; margin-bottom: 10px;">
          <!-- Bot Avatar -->
          <div class="message-avatar" v-if="message.type === 'bot'" style="margin-right: 10px;">
            <img src="./components/llama.png" alt="Bot Avatar" class="avatar" style="width: 35px; height: 35px;" />
          </div>

          <!-- Message Bubble -->
          <div class="message-bubble" style="max-width: 80%; background-color: #f1f1f1; padding: 10px; border-radius: 10px; text-align: left;">
            <!-- If the message contains markdown, render it with v-html -->
            <p v-if="message.isMarkdown" v-html="message.text" style="margin: 0; color: black;"></p>
            <!-- Otherwise, render it as plain text -->
            <p v-else style="margin: 0; color: black;">{{ message.text }}</p>
          </div>

          <!-- User Avatar -->
          <div class="message-avatar" v-if="message.type === 'user'" style="margin-left: 10px;">
            <v-icon size="35" color="black">mdi-account-circle</v-icon>
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
      <!-- 搜索框：根据选手名字筛选 -->
      <input
          type="text"
          v-model="searchQuery"
          placeholder="Search Players..."
          class="custom-input"
      />

      <select v-model="selectedRegion" class="custom-select">
        <option value="">All Regions</option>
        <option v-for="region in regions" :key="region" :value="region">
          {{ region }}
        </option>
      </select>
      <div v-for="(player, index) in filteredPlayers" :key="index" :class="['player-card']">
        <div class="player-info">
          <div class="player-avatar" :style="{ backgroundColor: player.bgColor }">
            {{ player.avatarInitials }}
          </div>
          <div>
            <h3 class="player-name">{{ player.handle }} </h3>
            <p class="player-score">{{ player.name }}</p> <p class="player-score"> {{ player.region}}</p>
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
            <TeamDisplay :average="average" :team="selectedTeam"
                         @deletePlayer="deletePlayerFromTeam"
                         @show-champion="showModal"/>
          </v-sheet>
        </v-bottom-sheet>
      </div>
    </div>

    <TrophyModal
        v-if="isModalVisible"
        :isVisible="isModalVisible"
        @close="closeModal"
    />
  </div>
</template>
<script>
import TeamDisplay from "@/views/components/TeamDisplay.vue";
import { client } from "@gradio/client";
import global from "..//global.js";
import axios from 'axios';
import TrophyModal from "@/views/components/TrophyModal.vue";
import { marked } from 'marked';

export default {
  components: {
    TrophyModal,
    TeamDisplay
  },
  computed: {
    filteredPlayers() {
      return this.availablePlayers.filter((player) => {
        const matchesName = player.name
            ? player.name.toLowerCase().includes(this.searchQuery.toLowerCase())
            : false;

        const matchesRegion =
            !this.selectedRegion || player.region === this.selectedRegion;

        return matchesName && matchesRegion;
      });
    },
  },
  async created() {
    try {
      const response = await axios.get(global.DATABASE_LINK + '/players');
      this.availablePlayers = response.data.map(player => {
        // 获取玩家名字的前两个字母，并将其转换为大写
        const initials = player.name
            ? player.name.split(' ').map(word => word.charAt(0).toUpperCase()).join('').slice(0, 2)
            : player.handle.charAt(0).toUpperCase();

        // 随机生成一个背景颜色
        const colors = ['#e57373', '#81c784', '#64b5f6', '#ffb74d', '#ba68c8'];
        const bgColor = colors[Math.floor(Math.random() * colors.length)];

        return {
          ...player,
          avatarInitials: initials,
          bgColor,
        };
      });

      console.log(this.availablePlayers); // 检查输出的内容是否正确
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    const regionResponse = await axios.get(global.DATABASE_LINK + '/regions');
    const averageResponse = await axios.get(global.DATABASE_LINK + '/average');
    this.regions = regionResponse.data;
    this.average = averageResponse.data[0];
  },
  data() {
    return {
      isModalVisible: false,
      searchQuery: '',
      average: {},
      selectedRegion: '',
      regions: [],
      llmService: global.LLM_SERVICE_TPYE,
      selectedTeam: [],
      inputMessage: '',
      messages: [
        { type: 'bot', text: 'Yeah, it would help in forming a team!' },
      ],
      availablePlayers: [],
    };
  },
  methods: {
    showModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
    addPlayerToTeam(player) {
      if (this.selectedTeam.length < 6 && !this.selectedTeam.includes(player)) {
        this.selectedTeam.push(player);
      }
    },
    async sendMessage() {
      if (!this.inputMessage.trim()) return;
      this.messages.push({ type: 'user', text: this.inputMessage });
      const message = this.inputMessage;
      this.inputMessage = '';

      try {
        const app = await client(global.GRADIO_LOCAL_LINK);
        console.log('client config ok');
        const result = await app.predict("/chat", [message]);
        console.log('get chat result');
        const botResponse = result.data[0];
        console.log(botResponse);

        // Convert botResponse to markdown format using 'marked'
        const markdownResponse = marked(botResponse);

        this.messages.push({ type: 'bot', text: markdownResponse, isMarkdown: true });
      } catch (error) {
        this.messages.push({ type: 'bot', text: 'Sorry, I could not process your question at the moment.' });
        console.log(error);
      }
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
  text-align: left;
  display: flex;
  gap: 10px;
  align-items: center; /* 垂直居中 */
  height: 100%; /* 需要的高度 */
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
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 18px;
    font-weight: bold;
  }

.player-name {
  font-family: 'Bebas Neue', Impact, sans-serif; /* 选择一个粗体且霸气的字体 */
  font-size: 27px;
  color: #070602;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.player-score {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 14px;
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

/* 右边选手名字输入框 */
.custom-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 16px;
  outline: none;
}

.custom-input:focus {
  border-color: #007bff;
}
/* 右边选手赛区选择框 */
.custom-select {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 16px;
  outline: none;
  background-color: #fff;
}

.custom-select:focus {
  border-color: #007bff;
}
</style>
