<template>
  <div class="team-display">
    <div class="team-title">Your Team</div>
    <div class="team-grid">
      <PlayerCard
          v-for="(player, index) in team"
          :key="index"
          :player="player"
          @click="deletePlayer(player)"
      />
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
    team: {
      type: Array,
      required: true
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
  background-color: #2c2c2c;
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
  grid-template-columns: repeat(1, 1fr);
  gap: 10px;
}
</style>
