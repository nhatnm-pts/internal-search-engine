<template>
  <div class="search_bar">
    <input
      type="text"
      @click="onClick"
      @keyup.enter="onSearch"
    />
  </div>
</template>

<script>
import { useSearchResultStore } from "../store/searchResultStore";

export default {
  name: "SearchBar",
  methods: {
    onClick(ev) {
      ev.target.placeholder = "";
    },

    async onSearch(ev) {
      await useSearchResultStore.setStateData(ev.target.value);
    }
  }
}
</script>

<style scoped>
.search_bar {
  display: flex;
  z-index: 3;
  position: relative;
  min-height: 44px;
  background: #fff;
  border-radius: 24px;
  margin: 20px auto;
  width: 690px;
  border: 1px solid rgba(223, 225, 229, 0);
  box-shadow: 0 2px 8px 1px rgba(64, 60, 67, .24);
}

input {
  border: none;
  width: 660px;
  margin: auto;
  outline: none;
}

input:focus-visible {
  border: none !important;
}
</style>
