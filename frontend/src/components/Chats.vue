<template>
    <div class="chats-frame">
        <Chat 
            v-for="chat in chats"
            :key="chat.id"
            :chatName="chat.name"
            :lastMessage="chat.lastMessage"
            :chatIconName="chat.icon"
            :isActive="chat.id === currentChatId"
            @click="setCurrentChat(chat.id)">
        </Chat>
    </div>
</template>

<script setup>
import { useChatStore } from '@/chat-store';
import { onMounted, ref, computed } from 'vue'
import Chat from './Chat.vue'

const chatStore = useChatStore();
const chats = ref([]);

const currentChatId = computed(() => chatStore.currentChatID);

onMounted(load_chats);

async function load_chats(params) {
    try {
        const response = await fetch("../../mock/chats.json");
        const chatDB = await response.json();
        chats.value = chatDB.chats;
        chatStore.chats = chatDB.chats;
        
        if (chats.value.length > 0 && !currentChatId.value) {
            chatStore.setCurrentChat(chats.value[0].id);
        }
    } catch (error) {
        console.error('Error loading chats:', error);
    }
}

function setCurrentChat(id) {
    chatStore.setCurrentChat(id)
}
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .chats-frame {
        display: flex;
        flex-direction: column;

        height: fit-content;

        gap: 0.25rem;
        background-color: var(--primary-color);
        
        padding: 0.25rem;
        border-radius: 0.25rem;
    }
</style>
