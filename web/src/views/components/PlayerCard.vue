<template>
  <v-card class="player-card" elevation="3">
    <v-row no-gutters>
      <!-- 左侧：头像 -->
      <v-col cols="3"  class="text-center ">
        <div class="player-avatar" :style="{ backgroundColor: player.bgColor }">
          {{ player.avatarInitials }}
        </div>
      </v-col>

      <!-- 右侧：玩家信息和统计数据 -->
      <div></div>
      <v-col cols="9" >

        <div class="player-info">
          <v-card-title class="player-nickname text-h5" style="display: flex; justify-content: space-between; align-items: center;">{{ player.handle }}</v-card-title>
          <v-card-subtitle class="player-subtitle">{{ player.name }} -- {{ player.region }}</v-card-subtitle>

          <v-card-actions>
            <v-row dense>
              <v-col cols="4">
                <StatBar title="ACS " :value="player.average_combat_score" :avg="average.avg_combat_score" description="POOR" />
              </v-col>
              <v-col cols="4">
                <StatBar title="DDDelta" :value="player.average_dddelta" :avg="average.avg_dddelta" description="OKAY" />
              </v-col>
              <v-col cols="4">
                <StatBar title="KPR" :value="player.average_kpr" :avg="average.avg_kpr" description="OKAY" unit="%" />
              </v-col>
              <v-col cols="4">
                <StatBar title="Damage Cause" :value="player.average_damage_per_round" :avg="average.average_damage_per_round" description="POOR" />
              </v-col>
              <v-col cols="4">
                <StatBar title="Damage Taken" :value="player.average_damage_taken_per_round" :avg="average.average_damage_taken_per_round" description="POOR" />
              </v-col>
              <v-col cols="4">
                <StatBar title="HS Rate" :value="player.average_headshot_hit_rate" :avg="average.average_headshot_hit_rate" description="POOR" />
              </v-col>
            </v-row>
          </v-card-actions>
        </div>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import StatBar from './StatBar.vue';
import axios from "axios";  // 导入自定义的StatBar组件

export default {
  components: {
    StatBar
  },
  props: {
      average:{
        type: {},
        required: true
      },
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
  background-color: #2c2c2c;
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
.player-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 18px;
  font-weight: bold;
  margin-left: 15px;
  margin-top: 15px;
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
