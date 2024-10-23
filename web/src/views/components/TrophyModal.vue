<template>
  <transition name="modal">
    <div class="modal-overlay" v-if="isVisible" @click.self="close">
      <div class="modal-content">
        <div class="animation-container">
          <canvas ref="canvas" width="800" height="800"></canvas>
        </div>
        <button @click="close" class="close-button" aria-label="Close">
          ✕
        </button>
      </div>
    </div>
  </transition>
</template>

<script>
import {Rive} from '@rive-app/canvas';

export default {
  name: 'TrophyModal',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
  },
  data() {
    return {
      rive: null,
      riveAnimation: null
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    handleEsc(e) {
      if (e.key === 'Escape' && this.isVisible) {
        this.close();
      }
    },
    cleanupRive() {
      if (this.rive) {
        this.rive.cleanup();
        this.rive = null;
      }
    }
  },
  mounted() {
    document.addEventListener('keydown', this.handleEsc);
    new Rive({
      stateMachines: ['State Machine 1'],
      canvas: this.$refs.canvas,
      src: "src/trophy.riv",
      autoplay: true
    })
  },
  beforeDestroy() {
    document.removeEventListener('keydown', this.handleEsc);
    this.cleanupRive();
  }
};
</script>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(23, 21, 21, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.animation-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.animation-container canvas {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.close-button {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
  z-index: 10000;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter,
.modal-leave-to {
  opacity: 0;
}
</style>