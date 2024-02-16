<template>
  <p v-if="data.size > 0">Count: {{ data.size }}</p>
  <div
    class="container"
    :class="{'result': data.size > 0}"
  >
    <SearchHit
      v-for="element in data.result"
      :key="element.file_path"
      :data="{...element, query: data.query}"
    />
  </div>
</template>

<script>
import SearchHit from './SearchHit.vue';

export default {
  name: "SearchResult",
  props: {
    data: Object,
  },
  components: {
    SearchHit,
},
}
</script>

<style scoped>
p {
  margin: 20px auto;
}
.container {
  max-width: 85%;
  height: 44px;
  margin: 20px auto;
  border-radius: 24px;
  border: 1px solid rgba(223, 225, 229, 0);
  box-shadow: 0 2px 8px 1px rgba(64, 60, 67, .24);
  padding: 20px;
  overflow: scroll;
}

.result {
  height: 50vh !important;
  background-image: linear-gradient(to bottom right, rgba(255, 0, 0, 0.535), rgba(255, 196, 0, 0.502));
}
</style>
