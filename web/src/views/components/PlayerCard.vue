<template>
  <v-card class="player-card" elevation="3">
    <v-row no-gutters>
      <!-- 左侧：头像 -->
      <v-col cols="3"  class="text-center">
        <v-img
            height="100%"
            cover
        >
          <v-avatar
              color="grey"
              rounded="0"
              size="90"
          >
            <img src="./avatar.webp" cover height="100" width="100"></img>
          </v-avatar>
        </v-img>
      </v-col>

      <!-- 右侧：玩家信息和统计数据 -->
      <div></div>
      <v-col cols="9" >

        <div class="player-info">
          <v-card-title class="player-nickname text-h5" style="display: flex; justify-content: space-between; align-items: center;">{{ player.nickName }}
            <v-avatar>
            <img
                alt="John"
                src="./download.png"
                height="30"
                width="30"
            ></img>
          </v-avatar></v-card-title>
          <v-card-subtitle class="player-subtitle">{{ player.realName }} - {{ player.team }} - {{ player.age }} years</v-card-subtitle>

          <v-card-actions>
            <v-row dense>
              <v-col cols="4">
                <StatBar title="Rating 1.0" :value="player.rating" :avg="1.0" description="POOR" />
              </v-col>
              <v-col cols="4">
                <StatBar title="DPR" :value="player.dpr" :avg="0.65" description="OKAY" />
              </v-col>
              <v-col cols="4">
                <StatBar title="KAST" :value="player.kast" :avg="70" description="OKAY" unit="%" />
              </v-col>
<!--              <v-col cols="4">-->
<!--                <StatBar title="Impact" :value="player.impact" :avg="1.0" description="POOR" />-->
<!--              </v-col>-->
<!--              <v-col cols="4">-->
<!--                <StatBar title="ADR" :value="player.adr" :avg="80" description="POOR" />-->
<!--              </v-col>-->
<!--              <v-col cols="4">-->
<!--                <StatBar title="KPR" :value="player.kpr" :avg="0.7" description="POOR" />-->
<!--              </v-col>-->
            </v-row>
          </v-card-actions>
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import StatBar from './StatBar.vue';  // 导入自定义的StatBar组件

export default {
  components: {
    StatBar
  },
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
  padding: 3px;
}

/* 头像样式 */
.v-avatar {
  border: 2px solid white;
}

/* 玩家信息样式 */
.player-info {
  padding-left: 10px;
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
