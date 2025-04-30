<script setup lang="ts">
import type { PostOverview } from '../interfaces/PostSerializers';
import { fetchStaticData } from '../composables/fetchData';
import { userAuthStore } from '../stores/userAuthStore';

defineProps<PostOverview>();

const userStore = userAuthStore();

async function deleteItem(slug: string) {
  await fetchStaticData({
    url: `/post-mng/${slug}/`,
    method: 'DELETE',
    authToken: userStore.authToken,
    statusCode: 204,
  });
  window.location.reload();
}
</script>

<template>
  <div class="m-8 p-4 bg-b-1 rounded-2xl
    min-md:w-6/10 min-md:min-h-[250px] max-md:w-xs max-md:min-h-[500px]
    grid min-md:grid-cols-[85%_15%] max-md:grid-rows-[70%_30%]
    border-btn-1 border-2 shadow-btn-1 hover:shadow-md
    delay-150 duration-150">
    <div class="min-md:col-span-1 max-md:row-span-1 min-md:px-4 gap-2">
      <h2>{{ title }}</h2>
      <P>Published Date: <time>{{ pub_date }}</time></P>
      <p>{{ summary }}</p>
    </div>
    <div class=" flex gap-4
      min-md:flex-col justify-evenly items-center">
      <button class="base-btn-transition">PreView</button>
      <button class="base-btn-transition">Edit</button>
      <button @click="deleteItem(slug)" class="base-btn-transition">Delete</button>
    </div>
  </div>
</template>

<style scoped>
  @reference "../base.css";

  button {
    @apply flex justify-center items-center rounded-xl
      bg-btn-1 w-[80px] h-[30px] text-f-2;
  }
</style>