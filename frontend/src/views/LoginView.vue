<script setup lang="ts">
import { ref } from 'vue';
import { login as loginApi, register as registerApi } from '@/api';
import { useUserStore } from '@/stores/user';
import router from '@/router';

const username = ref();
const password = ref();
const userStore = useUserStore();

function login() {
  loginApi(username.value, password.value)
    .then(user => {
      userStore.user = user;
      router.push("/");
    })
    .catch((err) => {
      alert('Failed To Login')
    })
}

function register() {
  registerApi(username.value, password.value)
    .then(user => {
      userStore.user = user;
      router.push("/");
    })
    .catch((err) => {
      alert('Failed To Register')
    })
}

</script>

<template>
  <n-space justify="space-around">
    <n-card style="width: 550px;" title="Login / Register" size="huge">
      <template #cover>
        <img src="/widelogo.png" />
      </template>
      <p>
        Please Login! If you do not have an account, just enter your desired username and password and click Register!
      </p>
      <n-form>
        <n-form-item label="Username">
          <n-input v-model:value="username" placeholder="Input Username" />
        </n-form-item>
        <n-form-item label="Password">
          <n-input v-model:value="password" placeholder="Input Password" type="password" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-button-group size="large">
          <n-button @click="login()">Login</n-button>
          <n-button @click="register()">Register</n-button>
        </n-button-group>
      </template>
    </n-card>
    <n-card  style="width: 550px;" title="Welcome to Wager Whales!" size="huge">
      <template #header-extra>
        <img src="/tinylogo.png" class="mainlogo"/>
      </template>
      <h2>How to Play:</h2>
      <p>
        After logging into your account, navigate to any stream via the buttons at the top. 
        Once you are watching your desired stream, you may click and drag left-to-right on the stream to select an area.
        After, a dialog box will pop up prompting you to enter an amount to wager and a time, in seconds.
        Once you enter these values, your bet is placed, and if a fish travels within your selected region within your inputted time, you win!</p>
      <h3>Some things to note:</h3>
      <li>The larger the box, the lower the winning multiplier</li>
      <li>The larger the time, the lower the winning multiplier</li>
      <li>Click your amount (top right, green box) to see your active wagers</li>
      <li>Click our logo in the top left (Wager Whales) to view the site-wide leaderboard</li>
      <h1>Good Luck, Whales!</h1>
    </n-card>
  </n-space>
</template>
