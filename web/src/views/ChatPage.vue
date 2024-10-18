<template>
  <v-container>
    <v-row>
      <v-col cols="12" md = "12" lg="3" class="sidebar">
        <!-- 中间：展示用户选出的队伍 -->
        <TeamDisplay :team="selectedTeam" @deletePlayer="deletePlayerFromTeam"/>
      </v-col>
      <v-col cols="12" md = "12" lg = "5" class="chat-container">
        <!-- 左侧：聊天界面 -->
        <ChatBox :messages="messages" @sendMessage="handleSendMessage" />
      </v-col>
      <v-col cols="12" md = "12" lg ='3' class="sidebar">
        <!-- 右侧：展示可选择的选手 -->
        <PlayerSelection :availablePlayers="availablePlayers" @addPlayer="addPlayerToTeam" />
      </v-col>
    </v-row>

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
.sidebar {
  background-color: #6e6d6d;
  background: rgba(20, 20, 20, 0);
  padding: 20px;
  border-radius: 10px;
  margin: 10px;
  height: calc(100vh - 20px); /* 确保边栏填满整个高度 */
  overflow-y: auto;
}

.chat-container {
  backdrop-filter: blur(10px); /* 模糊效果 */
  background: rgba(20, 20, 20, 0.6);
  border-radius: 10px;
  height: calc(100vh - 20px); /* 确保聊天区域填满整个高度 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

</style>
