<template>
    <div class="user-card" v-on:click="updateInvitedUsers(userReference)">
        <div class="user-char-icon nunito-600" v-if="userIcon == null">{{  getChatDefaultIcon() }}</div>
        <div class="user-icon" v-else>{{ userIcon }}</div>
        <div class="user-name nunito-300">{{ userName }}</div>
        <div :color="userTag.replace('@', '#')" class="user-tag nunito-100">{{ userTag }}</div>
    </div>
</template>

<script setup>
const props = defineProps({
    invitedUsers: {
        type: Array,
        default: null,
    },
    userReference: null,
    userId: {
        type: Number,
        default: null,
    },
    userName: {
        type: String,
        default: "default",
    },
    userIcon: {
        type: String,
        default: null,
    },
    userTag: {
        type: String,
        default: "default",
    },
});
function getChatDefaultIcon()
{
    const words = props.userName.split(' ');
    let result = ""
    words.forEach(element => {
        result += element[0].toUpperCase();
    });
    return result;
}

const emits = defineEmits(['update:invitedUsers']);
const updateInvitedUsers = (newValue) => {
    emits('update:invitedUsers', newValue)
};

</script>

<style scoped>
    @import url("../css/colors.css");
    @import url("../css/fonts.css");

    .user-char-icon {
        display: flex;
        text-align: center;
        align-items: center;
        justify-content: center;

        border-radius: 50%;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color-deep));

        width: 1.5rem;
        height: 1.5rem;
    }

    .user-name {
        font-size: 0.8rem;
    }
    .user-tag {
        font-size: 0.6rem;
    }

    .user-card {
        display: flex;
        align-items: center;
        gap: 0.25rem;

        border-radius: 0.5rem;
        padding: 0.25rem;
        box-sizing: border-box;

        background-color: var(--grey-light-color);
        color: var(--white-color);
        width: 100%;
    }

    .user-card:hover {
        background-color: var(--primary-color);
    }
</style>
