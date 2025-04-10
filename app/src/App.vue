<template>
  <div class="flex flex-col">
    <HeaderLayer />
    <div class="z-0 my-[60px] min-h-[80vh]">
      <RouterView />
    </div>
    <div class="z-20">
      <FooterLayer />
    </div>
  </div>
</template>