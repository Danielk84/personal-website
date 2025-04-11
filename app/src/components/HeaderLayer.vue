<script setup lang="ts">
import { ref, onMounted } from 'vue';

const screenWidth = ref(window.innerWidth);
const flaodBar = ref(false)

onMounted(() => 
  window.addEventListener("resize", () => screenWidth.value = window.innerWidth)
);
</script>

<template>
  <header class="flex justify-center">
    <div class="bg-b-1 drop-shadow-xl/25 w-97/100 h-16 m-2 
      backdrop-blur-sm rounded-2xl
      flex justify-evenly items-center fixed z-10">

      <div class="icon"></div>

      <div v-if="screenWidth >= 700">
        <PagesBar />
      </div>
      <div v-else>
        <button @click="flaodBar = !flaodBar">
          <img src="../../public/menu.svg" alt="">
        </button>
      </div>

      <div class="flex">
        <FirstButton address="/post">Login</FirstButton>
        <SecondButton address="/post">SginUp</SecondButton>
      </div>
    </div>
  </header>
</template>