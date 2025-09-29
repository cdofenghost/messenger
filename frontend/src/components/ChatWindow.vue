<template>
    <div class="chat-container" v-if="currentChat">
        <div class="chat-bar">
            <div class="chat-icon">
                <img src="/src/static/imgs/666175.png"></img>
            </div>
            <div class="detail-info">
                <div class="chat-name nunito-600">{{ currentChat.name }} <span class="chat-type">({{currentChat.type}} Chat)</span></div>
                <div class="chat-member-count nunito-400">{{ members.length }} members</div>
            </div>
        </div>
        <div class="chat">
            <Message 
                v-for="message in messages"
                :key="message.id"
                :userSentMessage="message.sentByMe"
                :senderName="message.sender.name"
                :content="message.text"
                :timestamp="message.created_time"
                :withNewDate="message.withNewDate"
                :datestamp="message.datestamp">
            </Message>
            <div class="input-bar">
                <textarea @keyup.enter="addMessage" class="nunito-400" placeholder="Message" type="text" v-model="inputMessage"></textarea>
            </div>  
        </div>
    </div>
    
    <div class="chat-container empty-chat" v-else>
        <div class="empty-state">
            <div class="empty-icon">💬</div>
            <div class="empty-text nunito-600">Select a chat to start messaging</div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useChatStore } from '@/chat-store';
import Message from './Message.vue';

const chatStore = useChatStore();
const members = computed(() => chatStore.members);
const currentChat = computed(() => chatStore.currentChat);
const messages = computed(() => chatStore.messages);
var inputMessage = '';

function addMessage()
{
    // var message = { id: 32, senderId: 2, chat_id: currentChat, text: inputMessage, created_at: "19:00", updated_at: "19:00", sentByMe: true, senderName: "Andrew Neiman" }
    // messages.value.push(message);
    // inputMessage = '';  
}
</script>

<script>
    export default {
        data() {
            return {

            }
        }
    }
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .chat-type {
        color: var(--secondary-color); 
        font-size: 0.6rem;
        font-style: italic;
    }

    .chat-container {
        display: flex;
        flex-direction: column;

        background-color: var(--primary-color);
        border-radius: 0.25rem;
        font-size: 0.75rem;

        width: 100%;

        gap: 0.25rem;
        padding: 0.25rem;
        box-sizing: border-box;
    }

    .chat-icon {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        background-color: var(--accent-color);
        overflow: hidden;

        box-sizing: border-box;

    }
    .chat-icon img {
        max-height: 100%;
        max-width: 100%;

        box-sizing: border-box;
    }

    .chat-bar {
        display: flex;
        gap: 0.25rem;
        align-items: center;

        box-sizing: border-box;

    }

    .chat-member-count {
        color: var(--accent-color);
        font-size: 0.7rem;
    }

    .chat {
        display: flex;
        flex-direction: column;
        position: relative;
        gap: 0.25rem;

        background-color: var(--deep-color);
        color: var(--primary-color);

        width: 100%;
        height: 88vh;
        border-radius: 0.25rem;

        padding: 0.25rem 20%;
        overflow-x: hidden;
        overflow-y: scroll;
        
        scrollbar-color: var(--primary-color) var(--accent-color);
        scrollbar-width: thin;
        box-sizing: border-box;
    }

    .input-bar {
        position: sticky;
        bottom: 0;
        box-shadow: 0px 0px 16px 2px rgba(0, 0, 0, 35%);

        height: fit-content;
        max-height: 20vh;
        width: 100%;

        background-color: var(--primary-color);
        padding: 0.25rem;
        border-radius: 0.25rem;

        box-sizing: border-box;
    }

    .input-bar textarea {
        -ms-overflow-style: none;
        scrollbar-width: none;

        font-size: 0.7rem;
        border: none;
        outline: none;

        background-color: var(--primary-color);
        resize: none;
        field-sizing: content;

        width: 100%;
        max-height: 20vh;
        box-sizing: border-box;
    }

    .empty-chat {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    .empty-state {
        text-align: center;
        color: var(--accent-color);
    }

    .empty-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .empty-text {
        font-size: 1rem;
    }
</style>
