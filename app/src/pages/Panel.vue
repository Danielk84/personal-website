<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { userAuthStore } from '../stores/userAuthStore';

const userStore = userAuthStore();
const isLoading = ref(true);

onMounted(async () => {
  await userStore.fetchLoginAPI();
  setTimeout(() => isLoading.value = false, 1500);
});
</script>

<template>
  <LoadingScreen v-if="isLoading"></LoadingScreen>
  <div>
    <div>
      {{ userStore.authToken }}
    </div>
  </div>
</template>