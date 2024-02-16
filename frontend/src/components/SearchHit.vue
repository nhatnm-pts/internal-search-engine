<template>
  <div class="card">
    <p v-html="data.content" />
  </div>
</template>

<script>
export default {
  name: "SearchHit",
  props: {
    data: Object,
  },
}
</script>

<style scoped>
.card {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 5px 10px;
  background-color: #f3f3f3;
  margin: 10px;
  text-align: justify !important;
}
</style>
