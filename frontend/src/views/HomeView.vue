<script setup lang="ts">
import Header from '@/components/Header.vue';
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { self, streams as streamsApi, newWager as newWagerApi, wagers as wagersApi, users as usersApi } from '@/api';
import router from '@/router';
import { notifications } from '@/api';
import { useNotification } from 'naive-ui'
import { type User } from '@/generated/openapi';

const userStore = useUserStore();
const selectedStream = ref();
const streams = ref<any[]>([]);
const streamMap = ref<Map<string, string>>(new Map());
const wagers = ref<any>([]);
const wagerdivs = ref<any[]>([]);
if (!userStore.user) {
  self().then(user => {
    userStore.user = user;
    streamsApi()
      .then(streamItems => {
        streams.value = streamItems;
        selectedStream.value = streamItems[0].id;
        for (const stream of streamItems) {
            streamMap.value.set(stream.id, stream.label);
        }
      })
    wagersApi()
      .then(wagerItems => {
        wagers.value = wagerItems;
      })
  }).catch((err) => {
    router.push("/login");
  })
}

streamsApi()
  .then(streamItems => {
    streams.value = streamItems;
    selectedStream.value = streamItems[0].id;
    for (const stream of streamItems) {
      streamMap.value.set(stream.id, stream.label);
    }
  })
wagersApi()
  .then(wagerItems => {
    wagers.value = wagerItems;
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
const maxArea = 20000;
const minArea = 200;
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
    highlight.value!.classList.remove('shake');
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
const bet = ref();
const duration = ref();

function normalize(x: number, y: number) {
  var length = Math.sqrt(x**2+y**2);
  x = x/length;
  y = y/length;
  return [x * imageWidth, y * imageHeight];
}

function mouseUp(event: any) {
  if (selected) {
    selected = false;
    [selectStartX.value, selectStartY.value] = normalize(startX, startY);
    [selectEndX.value, selectEndY.value] = normalize(endX, endY);

    let width = Math.abs(selectEndX.value - selectStartX.value);
    let height = Math.abs(selectEndY.value - selectStartY.value);
    let area = width * height;
    if (minArea < area && area < maxArea) {
      bet.value = undefined;
      duration.value = undefined;
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
  if (bet.value == undefined || duration.value == undefined) {
    alert('Invalid Wager');
    return;
  }
  newWagerApi(selectStartX.value, selectStartY.value, selectEndX.value, selectEndY.value, bet.value, duration.value, selectedStream.value)
    .then((wager) => {
      wagers.value.push(wager);
      userStore.user.balance -= bet.value;
    })
    .catch((err) => {
      alert('Invalid Wager');
    })
}

const notification = useNotification();
setInterval(() => {
  notifications()
    .then(notifications => {
      for (const n of notifications) {
        if (n.delta < 0) {
          userStore.user.balance += n.delta;
          notification.error({
            content: n.message
          })
        } else {
          userStore.user.balance += n.delta;
          notification.success({
            content: n.message
          })
        }
      }
      if (notifications.length) {
        // if we got a notification, then some wager was closed, refresh them
        wagersApi().then(wagersItems => {
          wagers.value = wagersItems;
        })
      }
    })
}, 1000);

const leaderBoardVisible = ref(false);
const leaderboard = ref<User[]>([]);

function openLeaderboard() {
  usersApi()
    .then((usersItems) => {
      leaderboard.value = usersItems;
      leaderBoardVisible.value = true
    })
}

</script>

<template>
  <Header :buttons="streams" :selected="selectedStream" :select-func=selectStream :wagers="wagers" :stream-map="streamMap" :show-leaderboard="openLeaderboard" />
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
      aria-modal="true">
      <template #header-extra>
        <n-button @click="close()" type="error">Cancel</n-button>
      </template>
      <n-form>
        <n-form-item label="Wager">
          <n-input v-model:value="bet" placeholder="Enter Wager" type="number" />
        </n-form-item>
        <n-form-item label="Duration">
          <n-input v-model:value="duration" placeholder="Enter Duration (Seconds)" type="number" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-button @click="submit()" size="large" type="success">Submit</n-button>
      </template>
    </n-card>
  </n-modal>
  <n-modal v-model:show="leaderBoardVisible">
    <n-card
    style="width: 600px"
      title="Leaderboard"
      :bordered="false"
      size="huge"
      role="dialog"
      aria-modal="true">
      <template #header-extra>
        <n-button @click="leaderBoardVisible = false" type="error">Cancel</n-button>
      </template>
      <n-data-table :columns="[
        {'title':'Username', 'key': 'username'},
        {'title': 'Balance', 'key': 'balance'}
      ]"
      :data="leaderboard"/>
  </n-card>
  </n-modal>
</template>
