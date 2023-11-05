<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { darkTheme } from 'naive-ui'
</script>

<template>
  <n-config-provider :theme="darkTheme">
    <n-notification-provider>
      <n-space vertical size="large">
        <n-layout style="height: 100vh;">
          <n-layout-content content-style="padding: 24px;">
            <RouterView />
          </n-layout-content>
        </n-layout>
      </n-space>
    </n-notification-provider>
  </n-config-provider>
</template>