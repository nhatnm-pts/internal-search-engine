<template>
  <div class="card">
    <p v-html="boldingWords()" />
  </div>
</template>

<script>
export default {
  name: "SearchHit",
  props: {
    data: Object,
  },
  methods: {
    boldingWords() {
      const queryRegex = new RegExp(this.data.query, "gi");
      return this.data.content.replaceAll(
        queryRegex,
        `<b>${this.data.query}</b>`
      );
    }
  }
}
</script>

<style scoped>
.card {
  border: 1px solid transparent;
  border-radius: 4px;
  padding: 2px;
  background-color: #f3f3f3;
  margin: 10px;
  text-align: justify !important;
}
</style>
