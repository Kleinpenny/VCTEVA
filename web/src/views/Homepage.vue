<template>
  <div class="homepage-container">
    <!-- 浅黑色背景遮罩层 -->
    <div class="background-overlay"></div>
    <!-- 新增标题部分 -->
    <div class="title-section">
      <h1 class="main-title">VALORANT CHAMPION TEAM BUILDER</h1>
      <p class="sub-title">Use LLM to build winning teams for VALORANT Esports</p>
    </div>
    <div class="start-button">
      <!-- 使用 router-link 进行页面跳转 -->
      <router-link to="/test" class="start-now">Start Now</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name:"HomePage"
};
</script>

<style scoped>
.homepage-container {
  background-size: auto;  /* 确保背景覆盖整个页面 */
  height: 100%;  /* 视窗高度填充 */
  width: 100%;   /* 视窗宽度填充 */
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.title-section {
  position: relative; /* 使其位于遮罩层之上 */
  text-align: center;
  margin-bottom: 20px;
  color: white;
  z-index: 2; /* 确保文字在遮罩层之上 */
}

.main-title {
  font-size: 52px; /* 调整字体大小 */
  font-weight: 900; /* 设置为更粗的字体 */
  text-transform: uppercase;
}

.sub-title {
  font-size: 28px; /* 调整副标题字体大小 */
  font-weight: 700; /* 设置副标题为粗体 */
  text-transform: uppercase;
  margin-top: 10px;
  letter-spacing: 2px;
}

.start-now {
  position: relative; /* 确保按钮位于遮罩层之上 */
  font-size: 24px;
  padding: 15px 30px;
  background-color: white ;
  color: black;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 1s ease-out, transform 1s ease-out;
  z-index: 2; /* 确保按钮在遮罩层上方 */
}

.start-now:hover {
  background-color: #7c7c7c;
}

.chat-interface {

  margin-top: 50px;
}

/* 按钮点击后的动画效果 */
@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(50px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
