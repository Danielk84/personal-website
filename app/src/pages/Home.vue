<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { getStaticData } from '../composables/fetchData';
import type { PostOverview } from '../types/PostSerializers';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(true);
const content = ref<PostOverview[]>();

onMounted(async () => {
  try {
    const data = await getStaticData<PostOverview[]>("/posts/");
    if (data.statusCode !== 200) throw data;

    loading.value = false;
    content.value = data.data;
  } catch (error) {
    console.error(error)
    router.push("/404/");
  }
});
</script>

<template>
  <div class="content-box h-[50vh]">
    <h1>hello</h1>
  </div>
    <div class="ref-box ref-box-color overflow-auto">
      <PostBox />
      <PostBox />
      <PostBox />
      <PostBox />
      <PostBox />
    </div>
  <div class="content-box h-[600px]">
    <h2>this content box</h2>
  </div>
  <div class="ref-box ref-box-color">
    {{ content }}
  </div>
</template>

<style scoped>
  @reference "../base.css";

  .content-box {
    @apply flex justify-center items-center;
  }
  .ref-box {
    @apply drop-shadow-xl/25 h-fit p-4
      flex justify-evenly items-center flex-wrap;
  }
</style>