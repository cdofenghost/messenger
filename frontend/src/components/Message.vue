<template>
    <div v-if="!userSentMessage" class="other-message-container">
        <div class="message-sender nunito-800">
            <b>{{ senderName }}</b>
        </div>
        <div class="message-content">
            {{ content }}
        </div>
        <div class="timestamp">{{ timestamp }}</div>  
    </div>
    <div v-if="userSentMessage" class="your-message-container">
        <div class="message-sender nunito-800">
            <b>{{ senderName }}</b>
        </div>
        <div class="message-content">
            {{ content }}
        </div>
        <div class="timestamp">{{ timestamp }}</div>
    </div>
</template>

<script>
    export default {
        props: {
            userSentMessage: {
                type: Boolean,
                default: false
            },
            senderName: {
                type: String,
                default: 'Message Sender'
            },
            content: {
                type: String,
                default: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet eaque quas blanditiis velit iure. In placeat quam, suscipit ex vitae sequi culpa maiores rem quia itaque id officiis quo consequuntur."
            },
            timestamp: {
                type: String,
                default: "hh:mm"
            }
        }
    }
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .your-message-container {
        background-color: var(--accent-color);
        color: var(--primary-color);
        align-self: flex-end;

        width: fit-content;
        max-width: 90%;
        height: fit-content;

        padding: 0.25rem;
        border-radius: 0.25rem;
    }

    .other-message-container {
        background-color: var(--primary-color);
        color: black;

        width: fit-content;
        max-width: 90%;
        height: fit-content;

        padding: 0.25rem;
        border-radius: 0.25rem;
    }

    .your-message-container::selection {
        background-color: var(--primary-color);
        color: var(--deep-color);
    }

    .other-message-container .message-sender {
        font-size: 0.6rem;
        color: var(--accent-color);
    }
    .your-message-container .message-sender {
        font-size: 0.6rem;
        color: var(--primary-color);
    }

    .timestamp {
        font-size: 0.4rem;
        text-align: right;
        margin-top: 0.1rem;
    }

    .your-message-container .timestamp {
        color: var(--unnecessary-color-white);
    }

    .other-message-container .timestamp {
        color: var(--unnecessary-color-grey);
    }
</style>
