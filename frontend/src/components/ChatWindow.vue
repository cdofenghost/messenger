<template>
    <div class="chat-container" v-if="currentChat">
        <div class="chat-bar">
            <div class="chat-icon">
                <img src="/src/static/imgs/666175.png"></img>
            </div>
            <div class="detail-info" style="width: 100%; box-sizing: border-box;">
                <div class="chat-name nunito-600">{{ currentChat.name }} <span class="chat-type">({{currentChat.type}} Chat)</span></div>
                <div class="chat-member-count nunito-400">{{ members.length }} members</div>
            </div>
            <div class="mini-button"><font-awesome-icon icon='plus'></font-awesome-icon></div>
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

const headers = new Headers();
headers.append('Content-Type', 'application/json');

async function addMessage(event)
{
    console.log(inputMessage);  
    if (inputMessage.trim().length > 0 && !event.shiftKey)
    {
        try {
            const response = await fetch(`/api/chats/${chatStore.currentChatID}/messages`, {
                headers: headers,
                method: "POST",
                body: JSON.stringify({text: inputMessage}),
            });

            if (response.ok) 
            {
                var message = await response.json();
                message = chatStore.addNewMessage(message);
            }

            else throw new Error(response.json());
        } catch (error) {
            console.error(error);
        }
        inputMessage = '';  
    }
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
        color: var(--accent-color-deep); 
        font-size: 0.6rem;
        font-style: italic;
    }

    .mini-button {
        align-self: center;
        padding: 0.25rem;
        border-radius: 50%;

    }
    .mini-button:hover {
        background-color: var(--grey-color);
    }

    .chat-container {
        display: flex;
        flex-direction: column;

        background-color: var(--white-color);
        border: 2px solid var(--primary-color);
        box-shadow: 0px 0px 16px 2px rgba(0, 0, 0, 35%);
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
        background: linear-gradient(90deg, #7F56D9, #9E77ED);
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
        justify-content: space-between;

        box-sizing: border-box;
        border: 1px solid salmon;
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

        background: linear-gradient(45deg, var(--grey-color));
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

        background-color: var(--white-color);
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

        background-color: var(--white-color);
        caret-color: var(--primary-color);
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
