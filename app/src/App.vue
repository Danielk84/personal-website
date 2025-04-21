<template>
  <div class="flex flex-col bg-w-1 text-f-1">
    <HeaderLayer />
    <div class="z-0 my-[80px] min-h-[80vh]">
      <RouterView />
    </div>
    <div class="z-10">
      <FooterLayer />
    </div>
  </div>
</template>