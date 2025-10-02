<template>
    <div class="chat-frame"
        :class="{ 'active-chat': isActive }"
        @click="$emit('click')">
        <div class="chat-icon">
            <img :src="'/src/static/imgs/' + chatIconName"></img>
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
                default: "666175.png"
            },
            isActive: {
                type: Boolean,
                default: false
            }
        },
    }
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .last-msg-time {
        font-size: small;
    }

    .chat-frame:hover {
        background-color: var(--grey-color);

        transition: background-color 0.1s ease-in;
    }

    .chat-frame {
        background-color: var(--accent-color);
        border: 4px solid transparent;
        transition: background-color 0.3s ease-out;
    }

    .chat-frame.active-chat {
        color: var(--white-color);
        background-color: var(--accent-color-deep);
        border: 4px solid transparent;
    }

    .chat-frame {
        font-size: 0.7rem;

        display: flex;
        background-color: var(--white-color);
        border-radius: 0.5rem;

        color: var(--black-color);
        font-size: 0.75rem;
        padding: 0.25rem;

        align-items: center;
        display: flex;
        gap: 0.25rem;
    }
    
    .chat-info {
        width: 100%;
        display: flex;

        justify-content: space-between;
    }

    .chat-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(90deg, #7F56D9, #9E77ED);
        overflow: hidden;

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
    
</style>
