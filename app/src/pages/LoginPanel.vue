<script setup lang="ts">
import { userAuthStore } from '../stores/userAuthStore';

const userStore = userAuthStore();

const updateUsername = (value: string) => userStore.username = value;
const updatePassword = (value: string) => userStore.password = value;
</script>

<template>
  <div class="flex justify-center">
    <div class="ref-box-color sm:w-[60%] max-sm:w-[90%] h-[500px] my-20 rounded-2xl
      shadow-2xl shadow-b-2/100 flex flex-col justify-evenly items-center
      text-f-2">
      <div class="flex flex-col gap-4">
        <label for="username">Username:</label>
        <StyledInput :date="`${userStore.username}`" @setInput="updateUsername"/>
        <label for="password">Password:</label>
        <StyledInput :date="userStore.password" @setInput="updatePassword"
          type="password"/>
      </div>
      <FirstButton @click="userStore.fetchLoginAPI()" address="/panel">Login</FirstButton>
    </div>
  </div>
</template>