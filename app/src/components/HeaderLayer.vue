<script setup lang="ts">
import { ref, onMounted } from 'vue';

const screenWidth = ref(window.innerWidth);
const flaodBar = ref(false);

onMounted(() => 
  window.addEventListener("resize", () => screenWidth.value = window.innerWidth)
);
</script>

<template>
  <header class="flex justify-center">
    <div class="bg-b-1 drop-shadow-xl/25 w-97/100 h-16 m-2 
      backdrop-blur-sm rounded-2xl
      flex justify-evenly items-center fixed z-20">

      <div class="icon"></div>

      <div v-if="screenWidth >= 700">
        <PagesBar />
      </div>
      <div v-else>
        <button @click="flaodBar = !flaodBar" class="base-btn-transition
          focus:drop-shadow-xl/25">
          <img class="size-12" src="../../public/menu.svg" alt="menu">
        </button>
      </div>

      <div class="flex">
        <div v-if="$route.path !== '/login-panel'">
          <FirstButton address="/login-panel">Login</FirstButton>
        </div>
        <div v-if="$route.path !== '/singup-panel'">
        <SecondButton address="/login-panel">SginUp</SecondButton>
        </div>
      </div>
    </div>
    <Transition name="slide-fade">
      <div v-if="screenWidth < 700 && flaodBar" class="w-90/100 min-h-11 h-fit 
        fixed top-20 z-20 bg-b-1
        rounded-b-2xl p-4 drop-shadow-2xl border-t-2 border-btn-1
        flex justify-center items-center ">
        <PagesBar />
      </div>
    </Transition>
  </header>
</template>

<style scoped>
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>