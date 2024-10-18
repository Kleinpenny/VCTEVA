<template>
  <v-card class="player-card" elevation="3">
    <v-row no-gutters align="center">

      <!-- 右侧：玩家信息和统计数据 -->
      <div></div>
      <v-col cols="12">
        <div class="player-info">
          <v-card-title class="player-nickname text-h5">{{ player.nickName }}</v-card-title>
          <v-card-subtitle class="player-subtitle">{{ player.realName }} - {{ player.team }} - {{ player.age }} years</v-card-subtitle>
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>
<script>

export default {
  props: {
    player: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
/* 卡片样式 */
.player-card {
  color: white;
  background-image: linear-gradient(136deg, #1b1f23, #3a4755);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  padding: 10px;
}

/* 头像样式 */
.v-avatar {
  border: 2px solid white;
}

/* 玩家信息样式 */
.player-info {
  padding-left: 20px;
}

/* 昵称样式 */
.player-nickname {
  font-size: 20px;
  font-weight: bold;
  color: #ffffff;
}

/* 副标题样式 */
.player-subtitle {
  font-size: 14px;
  color: #cccccc;
  margin-bottom: 10px;
}
</style>
