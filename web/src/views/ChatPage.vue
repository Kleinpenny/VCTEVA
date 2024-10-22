<template>
  <v-container id="chatPage">

      <div class="chat-section">
        <ChatBox :messages="messages" @sendMessage="handleSendMessage" />
      </div>
      <div class="player-list">
        <PlayerSelection :availablePlayers="availablePlayers" @addPlayer="addPlayerToTeam" />
      </div>

<!--  <v-row>-->
<!--    <v-col cols="12" md = "12" lg="3" class="sidebar">-->
<!--      &lt;!&ndash; 中间：展示用户选出的队伍 &ndash;&gt;-->
<!--      <TeamDisplay :team="selectedTeam" @deletePlayer="deletePlayerFromTeam"/>-->
<!--    </v-col>-->
<!--  </v-row>-->
  </v-container>
</template>

<script>
import ChatBox from './components/ChatBox.vue';
import TeamDisplay from './components/TeamDisplay.vue';
import PlayerSelection from './components/PlayerSelection.vue';

export default {
  components: {
    ChatBox,
    TeamDisplay,
    PlayerSelection
  },
  data() {
    return {
      messages: [
        { type: 'bot', text: 'Welcome to the Esports Chat!' },
      ],
      selectedTeam: [],
      availablePlayers: [
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
      ]
    };
  },
  methods: {
    handleSendMessage(message) {
      if (!message) return;
      this.messages.push({type: 'user', text: message});
      this.messages.push({type: 'bot', text: `Bot response to: "${message}"`});
    },
    addPlayerToTeam(player) {
      if (this.selectedTeam.length < 6 && !this.selectedTeam.includes(player)) {
        this.selectedTeam.push(player);
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
#chatPage {
    color: #fff; /* 白色字体以便在深色背景上可见 */
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-size: cover; /* 确保背景图片覆盖整个视窗 */
    background-color: white;
    width: 100vw;

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
/* 聊天区域样式 */
.chat-section {
  width: 60%; /* 调整聊天区的宽度 */
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 玩家列表样式 */
.player-list {
  width: 35%;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}


</style>
