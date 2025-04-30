<script setup lang="ts">
import { ref } from 'vue';

const isLoading = ref(true);
</script>

<template>
  <LoadingScreen v-if="isLoading"></LoadingScreen>
  <div>
    <div>
      asdasdd
    </div>
  </div>
</template>