<script setup lang="ts">
import { onMounted, ref } from 'vue';
import type { PostOverview } from '../interfaces/PostSerializers';
import type BasePagination from '../interfaces/BasePagination';
import { getStaticData } from '../composables/fetchData';
import { useRouter } from 'vue-router';

const router = useRouter();
const contents = ref<PostOverview[]>();

onMounted(async () => {
  try {
    const { json, statusCode, msg } = await getStaticData("/posts/");
    if (statusCode !== 200) throw msg;

    contents.value = (json as BasePagination<PostOverview>).results;
  } catch (error) {
    router.push(`/404/${error}`);
  }
});
</script>

<template>
  <div v-if="contents">
    <div class="grid grid-cols-1 w-screen">
      <div v-for="content in contents">
        <PostOverview :title="content.title" :slug="content.slug" :user="content.user"
          :summary="content.summary" :pub_date="content.pub_date" />
      </div>
    </div>
  </div>
  <div>
    <PaginationManager />
  </div>
</template>