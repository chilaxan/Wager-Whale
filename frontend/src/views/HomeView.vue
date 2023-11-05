<script setup lang="ts">
import Header from '@/components/Header.vue';
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { self, streams as streamsApi } from '@/api';
import router from '@/router';

const userStore = useUserStore();
if (!userStore.user) {
  self().then(user => {
    userStore.user = user;
    streamsApi()
      .then(streamItems => {
        streams.value = streamItems;
        selected.value = streamItems[0].id;
      })
  }).catch((err) => {
    router.push("/login");
  })
}
const selected = ref();
const streams = ref<any[]>([])

streamsApi()
  .then(streamItems => {
    streams.value = streamItems;
    selected.value = streamItems[0].id;
  })

function selectStream(stream: any) {
  console.log(stream);
  selected.value = stream.id;
}


</script>

<template>
  <Header :buttons="streams" :selected="selected" :select-func=selectStream />
  <div style="max-width: 100%; text-align: center;">
    <img :src="`/api/streams/${selected}`" class="stream">
  </div>
</template>
