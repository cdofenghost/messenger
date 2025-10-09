<template>
    <div class="chat-frame"
        :class="{ 'active-chat': isActive }"
        @click="$emit('click')">
        <div class="chat-icon">
            <img v-if="chatIconName !== null" :src="'/src/static/imgs/' + chatIconName"></img>
            <div v-else class="icon-text-default nunito-600">{{ getChatDefaultIcon() }}</div>
        </div>
        <div class="chat-info">
            <div class="name-message">
                <div class="chat-name nunito-600">
                    {{ chatName }}
                </div>
                <div class="last-message nunito-300">
                    {{ lastMessage }}
                </div>
            </div>
            <div class="last-msg-time nunito-200">
                {{ lastTime }}
            </div>
        </div>
    </div>
</template>

<script setup>
</script>
<script>
    export default {
        props: {
            id: {
                type: Number,
                default: 0,
            },
            chatName: {
                type: String,
                default: "Chat Name",
            },
            lastMessage: {
                type: String,
                default: "Sender: Lore"
            },
            lastTime: {
                type: String,
                default: "2025-10-02T21:35:39.595845+07:00"
            },
            chatIconName: {
                type: String,
                default: null,
            },
            isActive: {
                type: Boolean,
                default: false
            }
        },
        methods: {
            getChatDefaultIcon()
            {
                const words = this.chatName.split(' ')
                let result = ""
                words.forEach(element => {
                    result += element[0].toUpperCase();
                });
                return result;
            }
        }
    }
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);
    
    .icon-text-default {
        text-align: center;
    }

    .last-msg-time {
        font-size: small;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;

        max-width: 10vw;
    }

    .chat-frame:hover {
        background-color: var(--grey-light-color);
        
        transition: background-color 0.1s ease-in;
    }

    .chat-frame {
        color: var(--white-color);

        border: 4px solid transparent;
        transition: background-color 0.3s ease-out;
    }

    .chat-frame.active-chat {
        background-color: var(--accent-color-deep);
        border: 4px solid transparent;
    }

    .chat-frame {
        font-size: 0.7rem;

        display: flex;
        background-color: var(--grey-color);
        border-radius: 0.5rem;

        font-size: 0.75rem;
        padding: 0.25rem;

        align-items: center;
        gap: 0.25rem;

        box-sizing: border-box;
        width: 100%;
    }
    
    .chat-info {
        width: 100%;
        display: flex;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        justify-content: space-between;
    }

    .chat-icon {
        box-shadow: 0px 0px 2px 1px rgba(0, 0, 0, 35%);
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color-deep));
        overflow: hidden;
        
        display: flex;
        align-items: center;
        justify-content: center;

        box-sizing: content-box;
        flex-shrink: 0;
    }

    .chat-icon img {
        max-height: 100%;
        max-width: 100%;
    }

    .last-message {
        font-size: 0.7rem;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;

        max-width: 10vw;
    }

    .chat-name {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;

        max-width: 10vw;
    }

    .name-message {
        white-space: nowrap;
        text-overflow: ellipsis;
        width: 100%;
    }
    
</style>
