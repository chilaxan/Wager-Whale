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
        selectedStream.value = streamItems[0].id;
      })
  }).catch((err) => {
    router.push("/login");
  })
}
const selectedStream = ref();
const streams = ref<any[]>([])

streamsApi()
  .then(streamItems => {
    streams.value = streamItems;
    selectedStream.value = streamItems[0].id;
  })

function selectStream(stream: any) {
  selectedStream.value = stream.id;
  highlight.value!.hidden = true;
}

var selected = false;
var startX: number, startY: number;
var endX: number, endY: number;
const imageHeight = 1080;
const imageWidth = 1920;
const maxArea = 800;
const minArea = 80;
const container = ref<HTMLDivElement>();
const highlight = ref<HTMLDivElement>();
const placeBet = ref(false);

function mouseDown(event: any) {
  if (!selected) {
    selected = true;
    startX = event.clientX //- container.value!.offsetLeft;
    startY = event.clientY //- container.value!.offsetTop;
    highlight.value!.style.left = `${startX}px`;
    highlight.value!.style.top = `${startY}px`;
    highlight.value!.style.width = `0px`;
    highlight.value!.style.height = `0px`;
    highlight.value!.hidden = false;
  }
}

function mouseMove(event: any) {
  if (selected) {
    endX = event.clientX //- container.value!.offsetLeft;
    endY = event.clientY //- container.value!.offsetTop;
    highlight.value!.style.width = `${endX - startX}px`;
    highlight.value!.style.height = `${endY - startY}px`;
  }
}

const selectStartX = ref();
const selectEndX = ref();
const selectStartY = ref();
const selectEndY = ref();

function mouseUp(event: any) {
  if (selected) {
    selected = false;
    selectStartX.value = (startX / imageWidth) * 100;
    selectStartY.value = (startY / imageHeight) * 100;
    selectEndX.value = (endX / imageWidth) * 100;
    selectEndY.value = (endY / imageHeight) * 100;

    let width = selectEndX.value - selectStartX.value;
    let height = selectEndY.value - selectStartY.value;
    let area = width * height;
    if (minArea < area && area < maxArea) {
      placeBet.value = true;
      highlight.value!.hidden = true;
    } else {
      highlight.value!.classList.add('shake');
      setTimeout(() => {
        highlight.value!.classList.remove('shake');
        highlight.value!.hidden = true;
      }, 500);
    }
  }
}

function close() {
  placeBet.value = false;
}

function submit() {
  placeBet.value = false;
  alert("Placeing Bet");
}

</script>

<template>
  <Header :buttons="streams" :selected="selectedStream" :select-func=selectStream />
  <div style="max-width: 100%; text-align: center;">
    <div id="highlight-box" hidden="true" ref="highlight"></div>
    <img
      :src="`/api/streams/${selectedStream}`"
      class="stream"
      id="image"
      ref="container"
      draggable="false" 
      @mousedown="mouseDown"
      @mousemove="mouseMove"
      @mouseup="mouseUp">
  </div>
  <n-modal v-model:show="placeBet">
    <n-card
      style="width: 600px"
      title="Place Bet"
      :bordered="false"
      size="huge"
      role="dialog"
      aria-modal="true"
      >
      <template #header-extra>
        <n-button @click="close()" type="error">Cancel</n-button>
      </template>
      Not Implemented Yet
      <template #action>
        <n-button @click="submit()" size="large" type="success">Submit</n-button>
      </template>
    </n-card>
  </n-modal>
</template>
