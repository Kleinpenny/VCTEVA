<template>
  <div>
    <div class="section-title">Select Players</div>

    <!-- 搜索框：用于根据选手名字筛选 -->
    <v-text-field
        v-model="searchQuery"
        label="Search Players"
        prepend-icon="mdi-magnify"
        outlined
        class="mb-3"
    ></v-text-field>

    <!-- 选择框：用于根据赛区筛选 -->
    <v-select
        v-model="selectedRegion"
        :items="regions"
        label="Select Region"
        prepend-icon="mdi-map-marker"
        outlined
        class="mb-4"
    ></v-select>

    <!-- 显示筛选后的选手列表 -->
    <div class="team-grid">
      <PlayerDenseCard
          v-for="(player, index) in filteredPlayers"
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
    PlayerDenseCard,
  },
  props: {
    availablePlayers: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      searchQuery: '',
      selectedRegion: null,
      regions: ['NA', 'EU', 'APAC', 'LATAM'], // 赛区列表
    };
  },
  computed: {
    filteredPlayers() {
      // 根据搜索框和赛区筛选选手
      return this.availablePlayers.filter((player) => {
        // 通过名字匹配
        const matchesName = player.nickName
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase());

        // 通过赛区匹配
        const matchesRegion =
            !this.selectedRegion || player.region === this.selectedRegion;

        // 同时满足名字和赛区筛选条件
        return matchesName && matchesRegion;
      });
    },
  },
  methods: {
    selectPlayer(player) {
      this.$emit('addPlayer', player);
    },
  },
};
</script>

<style scoped>
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
