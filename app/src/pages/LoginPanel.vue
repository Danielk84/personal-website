<template>
  <div class="flex justify-center">
    <div class="ref-box-color sm:w-[60%] max-sm:w-[90%] h-[500px] my-20 rounded-2xl
      shadow-2xl shadow-b-2/100 flex flex-col justify-evenly items-center
      text-f-2">
      <div class="flex flex-col gap-4">
        <label for="username">Username:</label>
        <Input />
        <label for="password">Password:</label>
        <Input />
      </div>
      <FirstButton address="/login-panel">Login</FirstButton>
    </div>
  </div>
</template>