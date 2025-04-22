import { ref, onMounted } from "vue";

export default function (){
  const screenWidth = ref(window.innerWidth);
  onMounted(() =>
    window.addEventListener("resize", () => screenWidth.value = window.innerWidth)
  );

  return { screenWidth };
}