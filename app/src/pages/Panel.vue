<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import type BasePagination from "../interfaces/BasePagination"; 
import type { PostOverview } from '../interfaces/PostSerializers';
import { userAuthStore } from '../stores/userAuthStore';
import { fetchStaticData } from '../composables/fetchData';

const router = useRouter();
const userStore = userAuthStore();
const isLoading = ref(true);
const contents = ref<PostOverview[]>();

onMounted(async () => {
  await userStore.fetchLoginAPI();
  try {
    const resp = await fetchStaticData(
      { url: "/post-mng/", authToken: userStore.authToken }
    );
    if ([403, 404].includes(resp.statusCode)) throw resp;

    contents.value = (resp.json as BasePagination<PostOverview>).results;
  } catch (error: any) {
    if (error.statusCode === 403)
      router.push(`/${(error.statusCode)}?msg=${error.msg || ""}`);
    else if (error.statusCode === 404) router.push("/login-panel");
  }
  setTimeout(() => isLoading.value = false, 1500);
});
</script>

<template>
  <LoadingScreen v-if="isLoading"></LoadingScreen>
  <div v-if="contents">
    <div v-for="content in contents" :key="content.pub_date"
      class="flex flex-col items-center">
      <PostOverviewMng :title="content.title" :user="content.user"
        :pub_date="content.pub_date" :summary="content.summary" :slug="content.slug" />
    </div>
    <PaginationManager />
  </div>
</template>