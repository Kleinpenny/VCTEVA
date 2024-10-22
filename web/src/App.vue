<template>
  <div id="app">

    <router-view></router-view> <!-- 显示路由组件 -->
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
/* 设置全局样式，包括暗色调的背景 */
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fff; /* 白色字体以便在深色背景上可见 */
  display: flex;
  justify-content: center;
  align-items: center;
  background: url('assets/background/app-egame.png') no-repeat center center fixed;
  background-size: cover; /* 确保背景图片覆盖整个视窗 */
}

</style>
