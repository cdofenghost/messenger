<template>
    <div class="chat-container" v-if="currentChat">
        <div class="chat-bar">
            <div class="chat-icon">
                <img v-if="chatIcon !== null"   src="/src/static/imgs/666175.png"></img>
                <div v-else class="icon-text-default nunito-600">{{ getChatDefaultIcon() }}</div>
            </div>
            <div class="detail-info" style="width: 100%; box-sizing: border-box;">
                <div class="chat-name nunito-600">{{ currentChat.name }} <span class="chat-type">({{currentChat.type}} Chat)</span></div>
                <div class="chat-member-count nunito-400">{{ members.length }} members</div>
            </div>
            <div class="mini-button" v-on:click="flipContent('settings')"><font-awesome-icon icon='ellipsis'></font-awesome-icon></div>
        </div>
        <div class="chat-inner-container">
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
                <div class="input-bar-handler">
                    <div class="input-bar">
                        <textarea @keyup.enter="addMessage" class="nunito-400" placeholder="Message" type="text" v-model="inputMessage"></textarea>
                        <div class="mini-button" v-on:click="addMessage">
                            <font-awesome-icon class="fa-icon" icon="paper-plane" style="rotate: 45deg; translate: -3px 1px; color: var(--accent-color-deep);"></font-awesome-icon>
                        </div>
                    </div>  
                </div>
            </div>
            <div class="chat-settings-bar" id="settings">
                <div class="chat-info">
                    <div class="chat-type nunito-400">{{ currentChat.type }} Chat Info</div>
                    <div class="chat-icon">
                        <img v-if="chatIcon !== null"   src="/src/static/imgs/666175.png"></img>
                        <div v-else class="icon-text-default nunito-600">{{ getChatDefaultIcon() }}</div>
                    </div>
                    <div class="chat-name nunito-600">{{ currentChat.name }}</div>
                    <div class="chat-member-count nunito-400">{{ members.length }} members</div>
                </div>
                <div class="button-bar">
                    <SwitchButton :style="{ textAlign: 'center' }" :text="'Members'"></SwitchButton>
                    <SwitchButton :text="'Media'"></SwitchButton>
                    <SwitchButton :text="'Files'"></SwitchButton>
                </div>
                <Suspense>
                    <ChatMembers 
                        :chatId="currentChat.id"
                        :key="`chat-members-${currentChat.id}`"></ChatMembers>
                </Suspense>
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
import SwitchButton from './SwitchButton.vue';
import ChatMembers from './ChatMembers.vue';

const chatStore = useChatStore();
const members = computed(() => chatStore.members);
const currentChat = computed(() => chatStore.currentChat);
const messages = computed(() => chatStore.messages);
var inputMessage = '';

const headers = new Headers();
headers.append('Content-Type', 'application/json');

const props = defineProps({
    chatIcon: {
        type: String,
        default: null,
    }
});

function getChatDefaultIcon()
{
    const words = currentChat.value.name.trim().split(' ')
    let result = ""
    words.forEach(element => {
        result += element[0].toUpperCase();
    });
    return result;
}

function flipContent(switchType)
{
    const hiddenContent = document.getElementById(switchType); 

    if (hiddenContent.classList.contains('show')) hiddenContent.classList.remove('show');
    else hiddenContent.classList.add('show');
}

async function addUser(params) {
    try {

    } catch (error) {

    }
}

async function addMessage(event)
{
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
                isOpen: false,
            }
        },
        methods: {
            togglePopup(params) {
                this.isOpen = !this.isOpen;
            }
        }
    }
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .chat-info {
        justify-items: center;
        padding: 8px;
    }
    
    .chat-info .chat-icon {
        width: 3rem;
        height: 3rem;
        min-width: 3rem;
        min-height: 3rem;
        margin: 8px;

        font-size: 1rem;
    }
    
    .chat-info .chat-type {
        width: 100%;
        color: var(--white-color);
        font-size: 0.7rem;
        font-style: normal;

        margin-bottom: 16px;
    }

    .chat-info .chat-member-count {
        color: #a3a3a3;
    }

    .button-bar {
        display: flex;
    }

    .chat-inner-container {
        display: flex;
        flex-grow: 1;
        height: 90%;
        box-sizing: border-box;
    }

    .chat-settings-bar {
        display: none;
		opacity: 0;

        background-color: var(--black-color);
        margin: 0 0.5rem;

		transition: all 0.1s ease;
		transition-property: overlay display opacity;
		transition-duration: 0.1s;
		transition-behavior: allow-discrete;
    }

	.show {
		display: block;

		opacity: 1;
		@starting-style {
			opacity: 0;
		}

        transition: all 0.1s ease-out;
	}

    .icon-text-default {
        text-align: center;
        color: var(--white-color);
    }

    .chat-type {
        color: var(--accent-color-deep); 
        font-size: 0.6rem;
        font-style: italic;
    }

    .mini-button {
        align-self: center;
        padding: 0.25rem;
        border-radius: 50%;

        transition: 0.2s ease-out background-color;
    }

    .mini-button:hover {
        background-color: var(--grey-light-color);
        transition: 0.1s ease-in background-color;
    }

    .chat-container {
        display: flex;
        flex-direction: column;

        background-color: var(--grey-color);
        font-size: 0.75rem;
        width: 100%;
        height: 100%;

        gap: 0.25rem;
        padding: 0.25rem 0.25rem;
        box-sizing: border-box;
    }

    .chat-icon {
        width: 2rem;
        height: 2rem;
        min-width: 2rem;
        min-height: 2rem;

        border-radius: 50%;
        background: linear-gradient(90deg, #7F56D9, #9E77ED);
        overflow: hidden;

        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;

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
    }

    .chat-member-count {
        font-size: 0.6rem;
    }

    .chat {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        position: relative;
        gap: 0.25rem;

        background: linear-gradient(45deg, var(--black-color));
        color: var(--primary-color);

        width: 100%;
        border-radius: 0.25rem;

        padding: 0.25rem 20%;
        overflow-x: hidden;
        overflow-y: auto;
        
        scrollbar-color: var(--accent-color-deep) var(--grey-color);
        scrollbar-width: thin;
        box-sizing: border-box;
    }

    .input-bar-handler {
        display: flex; 
        align-items: end; 
        justify-content: end;

        position: sticky; 
        bottom: 0; 
        height: 100%; 
    }

    .input-bar {
        display: flex;
        align-items: center;

        position: sticky;
        bottom: 0;
        box-shadow: 0px 4px 8px 1px rgba(0, 0, 0, 35%);

        height: fit-content;
        max-height: 20vh;
        width: 100%;

        background-color: var(--grey-color);
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

        background-color: var(--grey-color);
        caret-color: var(--primary-color);
        color: var(--white-color);

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
