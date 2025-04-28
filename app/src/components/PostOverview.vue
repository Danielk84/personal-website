<script setup lang="ts">
import type { PostOverview } from '../interfaces/PostSerializers';

defineProps<PostOverview>();
</script>

<template>
  <div class="flex justify-center">
    <RouterLink :to="`/post/${slug}/`" class="max-md:w-8/10 min-md:w-6/10">
      <div class="ref-box-color text-f-2 border-btn-1 m-4 px-4 py-8 rounded-xl
        min-h-[200px] delay-75 duration-150
        hover:scale-105 hover:drop-shadow-2xl hover:border-4">
      <h2>{{ title }}</h2>
      <p>{{ summary }}</p>
      <hr class="border-btn-1 border-2 my-4"/>
      <div class="flex flex-col items-center">
        <time>{{ pub_date }}</time>
        <p>{{ user }}</p>
      </div>
      </div>
    </RouterLink>
  </div>
</template>