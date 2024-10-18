<template>
  <div class="stat-bar">
    <div class="d-flex justify-space-between">
      <span class="stat-title">{{ title }}</span>
    </div>
    <v-progress-linear
        :location="null"
        bg-color="#92aed9"
        buffer-color="white"
        buffer-opacity="1"
        :buffer-value="getBarPercent() + 1"
        :color="getBarColor()"
        :class="getClassBar()"
        height="3"
        max="9"
        min="0"
        :model-value="getBarPercent()"
        rounded
    ></v-progress-linear>
    <div class="stat-description">{{ getDescription() }}</div>
  </div>
</template>

<script>
export default {
  data: () => ({ review: "20%" }),
  props: {
    title: String,
    value: Number,
    avg: Number,
    description: String,
    unit: {
      type: String,
      default: ''
    }
  },
  methods: {
    getBarPercent() {
      // 计算进度条的百分比
      return (this.value / (this.avg * 2)) * 100;
    },
    getBarColor() {
      // 根据数值返回颜色
      if (this.value >= this.avg * 1.2) {
        return 'green';
      } else if (this.value >= this.avg * 0.8) {
        return 'yellow';
      } else {
        return 'red';
      }
    },
    getClassBar() {
      if (this.value >= this.avg * 1.2) {
        return 'bg-green-lighten-1';
      } else if (this.value >= this.avg * 0.8) {
        return 'bg-amber-lighten-1';
      } else {
        return 'bg-red-lighten-1';
      }
    },
    getDescription() {
      // 根据数值返回颜色
      if (this.value >= this.avg * 1.2) {
        return 'GOOD';
      } else if (this.value >= this.avg * 0.8) {
        return 'OKAY';
      } else {
        return 'BAD';
      }
    }
  }
};
</script>

<style scoped>
.stat-bar {
  margin-bottom: 15px;
}

.stat-title {
  font-size: 12px;
  color: white;
}

.stat-value {
  font-size: 16px;
  font-weight: bold;
}

.stat-description {
  font-size: 12px;
  color: white;
  text-align: right;
  margin-top: 5px;
}
</style>
