<template>
  <div class="flex flex-col bg-w-1 text-f-1">
    <HeaderLayer class="z-30"/>
    <div class="my-[80px] min-h-[80vh]">
      <RouterView />
    </div>
    <FooterLayer class="z-10"/>
  </div>
</template>