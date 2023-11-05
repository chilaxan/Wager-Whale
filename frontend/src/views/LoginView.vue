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
  <div style="width: 550px; margin: 0 auto;">
    <n-card title="Login / Register" size="huge">
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
  </div>
</template>
