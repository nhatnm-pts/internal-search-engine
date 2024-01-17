import { reactive } from "vue";

export const useSearchResultStore = reactive({
  data: {},
  async setStateData(query) {
    const response = await fetch(
      `${process.env.VUE_APP_BASE_URL}/search/?query=${query}`,
      {
        headers: {
          "Content-Type": "application/json",
        }
      }
    );
    const responseJson = await response.json();
    this.data = {
      ...responseJson,
      query: query,
    };
  },
});
