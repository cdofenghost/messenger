import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useChatStore = defineStore('chat', () => {
    const currentUserID = 2;

    const currentChatID = ref(null);
    const chats = ref([]);
    const messages = ref([]);

    const currentChat = computed(() => {
        return chats.value.find(chat => chat.id === currentChatID.value)
    });

    function setCurrentChat(id) {
        currentChatID.value = id;
        loadMessages(id);
    }

    async function loadMessages(chatId) {
        try {
            const response = await fetch(`../mock/messages_${chatId}.json`);
            messages.value = (await response.json()).messages;
            messages.value.forEach(message => {
               message.sentByMe = currentUserID == message.sender_id;
            });
        } catch (error) {
            console.error('Error loading messages: ', error);
            messages.value = [];
        }
    }

    return {
        currentChatID,
        currentChat,
        chats,
        messages,
        setCurrentChat,
        loadMessages,
    }
});
