<template>
  <h1>Internal Search Engine</h1>
  <SearchBar />
  <SearchResult :data="useSearchResultStore.data" />
</template>

<script>
import { useSearchResultStore } from "./store/searchResultStore";
import SearchBar from "./components/SearchBar.vue";
import SearchResult from "./components/SearchResult.vue";

export default {
  name: "App",
  components: {
    SearchBar,
    SearchResult,
  },
  setup() {
    return { useSearchResultStore };
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  height: 90vh;
  overflow: hidden;
}
</style>
