<template>
  <div class="player-selection">
    <div class="section-title">Select Players</div>

        <v-text-field
            v-model="searchQuery"
            label="Search Players"
            prepend-icon="mdi-magnify"

            outlined
        ></v-text-field>

    <div class="team-grid">
      <PlayerDenseCard
          v-for="(player, index) in availablePlayers"
          :key="index"
          :player="player"
          @click="selectPlayer(player)"
      />
    </div>

  </div>
</template>

<script>
import PlayerDenseCard from './PlayerDenseCard.vue';

export default {
  components: {
    PlayerDenseCard
  },
  props: {
    availablePlayers: {
      type: Array,
      required: true
    }
  },
  computed: {
    filteredPlayers() {
      return this.availablePlayers;
    }
  },
  methods: {
    selectPlayer(player) {
      this.$emit('addPlayer', player);
    }
  }
};
</script>

<style scoped>
.player-selection {
  background-color: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
}

.section-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}
.team-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 20px;
}

.v-row {
  gap: 20px; /* 调整卡片之间的间距 */
}
</style>
