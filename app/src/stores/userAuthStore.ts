import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import type { UserAuthState } from "../interfaces/UserAuthState";
import { fetchStaticData } from "../composables/fetchData";

export const userAuthStore = defineStore("user-auth", {
  state: (): UserAuthState => {
    return {
      username: "",
      password: "",
      token: "",
      isAdmin: false,
    }
  },
  getters: {
    authToken: (state): string => `Token ${state.token}`,
  },
  actions: {
    async fetchLoginAPI() {
      try {
        const resp = await fetchStaticData<{ Token: string }>(
          "/user-panel/login/", "POST",
          JSON.stringify({ username: this.username, password: this.password }),
        );

        this.token = resp.json?.Token as string;
      } catch(error: any) {
        useRouter().push(
          `/login-panel/?json=${JSON.stringify(error.json)}&msg=${error.msg}`,
        );
      }
    },
  },
});