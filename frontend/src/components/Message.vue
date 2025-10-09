<template>
    <div class="date-blob" v-if="withNewDate">
        {{ datestamp }}
    </div>
    <div ref="targetComponent" v-if="!userSentMessage" class="other-message-container">
        <div class="message-sender nunito-800">
            <b>{{ senderName }}</b>
        </div>
        <div class="message-content nunito-300">
            {{ content }}
        </div>
        <div class="timestamp nunito-100">{{ timestamp }}</div>  
    </div>
    <div ref="targetComponent" v-else class="your-message-container">
        <div class="message-sender nunito-800">
            <b>{{ senderName }}</b>
        </div>
        <div class="message-content nunito-300">
            {{ content }}
        </div>
        <div class="timestamp nunito-100">{{ timestamp }}</div>
    </div>
</template>

<script>
    export default {
        mounted() {
            this.$refs.targetComponent.scrollIntoView({ behavior: 'smooth'});
        },
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
            },
            withNewDate: {
                type: Boolean,
                default: false,
            },
            datestamp: {
                type: String,
                default: "datestamp"
            }
        }
    }
</script>

<style scoped>
    @import url(../css/fonts.css);
    @import url(../css/colors.css);

    .message-content {
        font-size: 0.7rem;
    }

    .date-blob {
        position: sticky;
        text-align: center;
        align-self: center;

        background-color: var(--grey-color);
        color: var(--white-color);

        padding: 0.25rem;
        border-radius: 0.25rem;

        width: fit-content;
    }

    .your-message-container {
        background-color: var(--accent-color-deep);
        color: var(--white-color);
        align-self: flex-end;

        width: fit-content;
        max-width: 90%;
        height: fit-content;
        white-space: pre-wrap;

        padding: 0.25rem;
        border-radius: 0.5rem;
    }

    .other-message-container {
        background-color: var(--grey-color);
        color: var(--white-color);

        width: fit-content;
        max-width: 90%;
        height: fit-content;
        white-space: pre-wrap;  

        padding: 0.25rem;
        border-radius: 0.5rem;
    }

    .your-message-container::selection {
        background-color: var(--primary-color);
        color: var(--deep-color);
    }

    .other-message-container .message-sender {
        font-size: 0.6rem;
    }

    .your-message-container .message-sender {
        font-size: 0.6rem;
        color: var(--white-color);
    }

    .timestamp {
        font-size: 0.4rem;
        text-align: right;
        margin-top: 0.1rem;
    }

    .your-message-container .timestamp {
        color: var(--white-color);
    }

    .other-message-container .timestamp {
        color: var(--white-color);
    }
</style>
