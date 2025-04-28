<script setup lang="ts">
import type { PostOverview } from '../interfaces/PostSerializers';

defineProps<PostOverview>()
</script>

<template>
  <RouterLink :to="`/post/${slug}/`">
    <div class="bg-b-1 drop-shadow-xl/50 m-4 p-4
    min-sm:w-xs max-sm:w-8/10 h-[470px] rounded-xl
    transition-all delay-75 duration-150 ease-in-out
    hover:drop-shadow-none hover:scale-97">
    <div class="overflow-y-scroll">
      <h3>{{ title }}</h3>
      <p>{{ summary }}</p>
    </div>
    <hr class="border-btn-1 border-2 my-4"/>
    <p>{{ user }}</p>
    <time>{{ pub_date }}</time>
  </div>
  </RouterLink>
</template>