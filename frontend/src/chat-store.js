import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useUserStore } from './user-store';

export const useChatStore = defineStore('chat', () => {
    const currentChatID = ref(null);
    const chats = ref([]);
    const members = ref([]);
    const messages = ref([]);
    
    const datestampFormat = new Intl.DateTimeFormat('en-US', {
        month: "long",
        day: "numeric",
        year: "numeric",
    });

    const timeFormat = new Intl.DateTimeFormat('en-US', {
        hour: '2-digit',
        minute: '2-digit',
    });

    const currentChat = computed(() => {
        return chats.value.find(chat => chat.id === currentChatID.value)
    });

    function setCurrentChat(id) {
        currentChatID.value = id;
        loadMessages(id);
        getCurrentChatMembers(id);
    }

    async function loadMessages(chatId) {
        try {
            const response = await fetch(`/api/chats/${chatId}/messages`);
            messages.value = (await response.json());
            console.log(messages);

            var lastDate = new Date();
            lastDate.setTime(0);

            messages.value.forEach(message => {               
                var date = new Date(message.created_at);
                message.created_time = timeFormat.format(date);

                const diffTime = Math.abs(date - lastDate);
                const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

                if (diffDays >= 1)
                {
                    message.datestamp = datestampFormat.format(date);
                    message.withNewDate = true;
                    lastDate = date;
                    lastDate.setHours(0);
                    lastDate.setMinutes(0);
                    lastDate.setSeconds(0);
                    lastDate.setMilliseconds(0);
                }

                else console.log(diffDays);
                message.sentByMe = useUserStore().userData.id == message.sender.id;
            });
        } catch (error) {
            console.error('Error loading messages: ', error);
            messages.value = [];
        }
    }

    async function getCurrentChatMembers(chatId) {
        try {
            const response = await fetch(`/api/chats/${chatId}/members`);
            members.value = await response.json();
        } catch (error) {
            console.log(error);
        }
    }

    function addNewMessage(message)
    {
        const lastMessage = messages.value[messages.value.length -1];
        const lastDate = new Date(lastMessage.created_at);

        var date = new Date(message.created_at);
        message.created_time = timeFormat.format(date);

        const diffTime = Math.abs(date - lastDate);
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays >= 1)
        {
            message.datestamp = datestampFormat.format(date);
            message.withNewDate = true;
        }

        else console.log(diffDays);
        message.sentByMe = useUserStore().userData.id == message.sender.id;

        messages.value.push(message);
    }

    return {
        currentChatID,
        currentChat,
        chats,
        messages,
        members,
        setCurrentChat,
        loadMessages,
        addNewMessage
    }
});
