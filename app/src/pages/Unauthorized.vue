<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

onMounted(() =>
  setTimeout(() => router.push("/login-panel"), 10000)
);
</script>

<template>
  <div class="my-16 mx-8 flex flex-col gap-8 justify-center items-center">
    <h1>401 <span class="text-nowrap">http-Error</span></h1>
    <P class="text-2xl">You are not authenticated, you can go to the login page or wait 10 seconds.</P>
  </div>
</template>