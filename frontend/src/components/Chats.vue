<template>
    <div class="chats-frame">
        <Chat 
            v-for="chat in chats"
            :key="chat.id"
            :chatName="chat.name"
            :lastMessage="`${chat.last_message?.sender?.name || 'sender'}: ${chat.last_message?.text || 'text'}`"
            :lastTime="timeFormat.format(new Date(chat.last_message?.created_at || null)) || 'sender'"
            :chatIconName="chat.icon"
            :isActive="chat.id === currentChatId"
            @click="setCurrentChat(chat.id)">
        </Chat>
    </div>
</template>

<script setup>
import { useChatStore } from '@/chat-store';
import { useUserStore } from '@/user-store';
import { onMounted, ref, computed } from 'vue'
import Chat from './Chat.vue'

const timeFormat = new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
});

const chatStore = useChatStore();
const chats = ref([]);
const currentChatId = computed(() => chatStore.currentChatID);

onMounted(load_chats);

async function load_chats(params) {
    try {
        const response = await fetch("/api/users/me/chats");
        const chatDB = await response.json();
        console.log(chatDB);
        chats.value = chatDB;
        chatStore.chats = chatDB;
        
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
        background-color: var(--white-color);
        border: 2px solid var(--primary-color);  
              
        padding: 0.25rem;
        border-radius: 0.25rem;
    }
</style>
