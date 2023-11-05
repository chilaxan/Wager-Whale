<script setup lang="ts">
import { logout as logoutApi} from "@/api";
import router from "@/router";
import { useUserStore } from "@/stores/user";
import { ref } from "vue";

const userStore = useUserStore();
const props = defineProps({
    buttons: Array<{
        label: String,
        id: String,
        weight: Number,
    }>,
    selected: String,
    selectFunc: Function
})

function logout() {
    logoutApi().then(() => {
        router.push('/login');
    })
}

const showModal = ref(false);

</script>

<template>
    <n-space justify="space-between" size="large">
        <img src="/logo.png" class="mainlogo" />
        <n-button-group size="large">
            <n-button 
                v-for="button of buttons"
                @click="selectFunc!(button)"
                :type="selected == button.id ? 'warning' : ''">
                {{ button.label }}: {{ button.weight }}
            </n-button>
        </n-button-group>
        <n-button-group size="large">
            <n-button type="success" @click="showModal = true">
                ${{ userStore.user?.balance }}
            </n-button>
            <n-button type="info" @click="showModal = true">
                {{ userStore.user?.username }}
            </n-button>
            <n-button type="error" @click="logout()">
                Logout
            </n-button>
        </n-button-group>
    </n-space>
    <n-divider />
    <n-modal v-model:show="showModal">
        <n-card
        style="width: 600px"
        title="Manage Bets"
        :bordered="false"
        size="huge"
        role="dialog"
        aria-modal="true"
        >
        <template #header-extra>
            Not Implemented Yet
        </template>
        Not Implemented Yet
        <template #footer>
            Not Implemented Yet
        </template>
        </n-card>
    </n-modal>
</template>