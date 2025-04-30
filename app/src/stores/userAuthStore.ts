import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import type { UserAuthState } from "../interfaces/UserAuthState";
import { fetchStaticData } from "../composables/fetchData";


export const userAuthStore = defineStore("userAuth", {
  state: (): UserAuthState => {
    const oldState = localStorage.getItem("userAuth");
    if (oldState) return JSON.parse(oldState as string);

    return {
      username: "",
      password: "",
      token: "",
      isAdmin: false,
    }
  },
  getters: {
    authToken: (state): string => {
      if (state.token) return `Token ${state.token}`;
      return "";
    },
  },
  actions: {
    async fetchLoginAPI() {
      const router = useRouter();
      try {
        const resp = await fetchStaticData<{ Token: string }>({
          url: "/user-panel/login/",
          method: "POST",
          data: JSON.stringify({ username: this.username, password: this.password }),
        });
        if ([400, 403, 404].includes(resp.statusCode)) throw resp;
        
        this.token = resp.json?.Token as string;
      } catch(error: any) {
        const json = error?.json || {};
        const msg = error?.msg || 'Unknown error';
        router.push(
          `/login-panel?json=${JSON.stringify(json)}&msg=${msg}`,
        );
      }
    },
  },
});