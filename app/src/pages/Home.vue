<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import type { PostOverview } from '../interfaces/PostSerializers';
import { fetchStaticData } from '../composables/fetchData';

const router = useRouter();
const loading = ref(true);
const contents = ref<any>();

onMounted(async () => {
  try {
    const resp = await fetchStaticData<PostOverview[]>("/posts/overview/");

    contents.value = resp.json;
    loading.value = false;
  } catch (error: any) {
    router.push(`/404/${error.msg}/`);
  }
});
</script>

<template>
  <div class="content-box h-[50vh]">
    <h1>hello</h1>
  </div>
  <div v-if="!loading" class="ref-box ref-box-color overflow-auto">
    <div v-for="content in contents">
    <PostBox :title="content.title" :slug="content.slug" :pub_date="content.pub_date"
      :summary="content.summary" :user="content.user"/>
    </div>
  </div>
  <div class="content-box h-[600px]">
    <h2>this content box</h2>
  </div>
  <div class="ref-box ref-box-color">
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