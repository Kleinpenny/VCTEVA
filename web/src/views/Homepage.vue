<template>
  <div class="homepage-container">
    <div class="background-overlay"></div>
    <div class="content-wrapper">
      <div class="title-section">
        <h1 class="main-title">VALORANT CHAMPION TEAM BUILDER</h1>
        <p class="sub-title">Use LLM to build winning teams for VALORANT Esports</p>
      </div>
      <div class="start-button">
        <router-link to="/chat" class="start-now">Start Now</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage"
};
</script>

<style scoped>
.homepage-container {
  position: relative;
  height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1;
}

.content-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  transform: translateY(-15%); /* 将整个内容块向上移动 */
  max-width: 90%;
  width: 100%;
}

.title-section {
  text-align: center;
  margin-bottom: 3rem;
  color: white;
  animation: fadeInDown 1s ease-out;
}

.main-title {
  font-size: clamp(2rem, 5vw, 4rem); /* 响应式字体大小 */
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 1.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.sub-title {
  font-size: clamp(1rem, 2.5vw, 1.75rem);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.9;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.start-button {
  margin-top: 1rem;
  animation: fadeInUp 1s ease-out 0.5s both;
}

.start-now {
  display: inline-block;
  font-size: 1.25rem;
  font-weight: 600;
  padding: 1rem 2.5rem;
  background-color: white;
  color: black;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.start-now:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 添加媒体查询以确保在小屏幕上的响应式布局 */
@media (max-width: 768px) {
  .content-wrapper {
    transform: translateY(-10%);
    padding: 0 1rem;
  }

  .title-section {
    margin-bottom: 2rem;
  }
}
</style>