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
      <div class="champion-message" v-if="team.length >= 5">

        <v-btn size="x-large"  class="flex-grow-1 text-none mb-4" @click="handleShowChampion">
          Chase Your Champion
          <v-icon large color="yellow">mdi-trophy</v-icon>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
import PlayerCard from './PlayerCard.vue';

export default {
  components: {
    PlayerCard,
  },
  props: {
    average: {
      type: Object,
      required: true,
    },
    team: {
      type: Array,
      required: true,
      validator(value) {
        return value.length <= 5;
      },
    },
  },
  data() {
    return {
      isModalVisible: false,
      championImage: 'champion.webp', // 替换为实际图片路径
    };
  },
  computed: {
    limitedTeam() {
      return this.team.slice(0, 5);
    },
  },
  methods: {
    handleShowChampion() {
      // 触发事件到父组件
      this.$emit('show-champion');
    },
    deletePlayer(player) {
      this.$emit('deletePlayer', player);
    },
    showChampion() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
  },
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
  grid-column: span 1;
  text-align: center;
  align-content: center;
  justify-content: center;
}

.champion-button {
  background-color: #ffd700;
  border: none;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: transform 0.2s;
}

.champion-button:hover {
  transform: scale(1.05);
}
</style>
