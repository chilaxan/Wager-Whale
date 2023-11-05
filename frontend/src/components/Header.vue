<script setup lang="ts">
import { logout as logoutApi} from "@/api";
import { type Stream, type Wager } from "@/generated/openapi";
import router from "@/router";
import { useUserStore } from "@/stores/user";
import { ref, watch } from "vue";

const userStore = useUserStore();
const props = defineProps({
    buttons: Array<Stream>,
    selected: String,
    selectFunc: Function,
    wagers: Array<Wager>,
    streamMap: Map<String, String>,
    showLeaderboard: Function
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
        <img src="/logo.png" class="mainlogo" @click="showLeaderboard!()"/>
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
        <n-button v-for="wager of wagers">Wager: ${{ wager.bet }}, Duration: {{ wager.duration }}, Stream: {{ streamMap!.get(wager.stream) }}</n-button>
        <n-empty v-if="wagers?.length == 0"></n-empty>
        </n-card>
    </n-modal>
</template>