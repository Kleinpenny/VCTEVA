<template>
  <div class="team-display">
    <div class="team-title">Your Team</div>
    <div class="team-grid">
      <PlayerCard
          v-for="(player, index) in limitedTeam"
          :key="index"
          :player="player"
          :average="average"
          @click="deletePlayer(player)"
      />
      <div class="team-grid" v-if="team.length >= 5">
        Chase Your Champion
        <v-icon large color="yellow">mdi-trophy</v-icon>
      </div>
    </div>
  </div>
</template>

<script>
import PlayerCard from './PlayerCard.vue';

export default {
  components: {
    PlayerCard
  },
  props: {
    average:{
      type: {},
      required: true
    },
    team: {
      type: Array,
      required: true,
      validator(value) {
        // 验证 team 的长度不超过 5
        return value.length <= 5;
      }
    }
  },
  computed: {
    limitedTeam() {
      // 返回最多前 5 个玩家
      return this.team.slice(0, 5);
    }
  },
  methods: {
    deletePlayer(player) {
      this.$emit('deletePlayer', player);
    }
  }
};
</script>

<style scoped>
.team-display {
  display: flex;
  flex-direction: column;
  padding: 20px;
  border-radius: 10px;
}

.team-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.champion-message {
  grid-column: span 3; /* 占据整个行 */
  text-align: center;
  font-size: 18px;
  color: #ff0000;
  margin-top: 10px;
}
</style>
