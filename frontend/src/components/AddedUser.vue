<template>
    <div class="user-container">
        <div class="user-icon" v-if="userIcon != null"></div>
        <div class="user-text-icon nunito-400" v-else>{{ getChatDefaultIcon() }}</div>
        <div class="user-name nunito-200">{{ userName }}</div>
        <div class="cancel-button" v-on:click="deleleUser(userReference)"><font-awesome-icon icon="xmark" style="scale: 0.75; translate: -0.15px 1.2px;"></font-awesome-icon></div>
    </div>
</template>

<script setup>
    const props = defineProps({
        userReference: null,
        userId: {
            type: Number,
            default: null,
        },
        userIcon: {
            type: String,
            default: null,
        },
        userName: {
            type: String,
            default: null,
        }
    });

    const emits = defineEmits("delete");
    const deleleUser = (userToDelete) => {
        emits("delete", userToDelete);
    };

    function getChatDefaultIcon()
    {
        const words = props.userName.split(' ');
        let result = "";
        words.forEach(element => {
            result += element[0].toUpperCase();
        });
        return result;
    }

</script>

<style scoped>
    @import url("../css/colors.css");
    @import url("../css/fonts.css");

    .cancel-button {
        background-color: var(--error-color);
        border-radius: 50%;
    }

    .cancel-button:hover { 
        background-color: var(--white-color);
        color: var(--error-color);

        transition: 0.1s ease-in all;
    }

    .user-container {
        display: flex;
        align-items: center;

        gap: 0.125rem;
        font-size: 0.6rem;

        background-color: var(--grey-light-color);
        padding: 0.125rem;
        border-radius: 0.25rem;
    }
    .user-container:start {
        background-color: aqua;
        transition: 0.5s ease-in background-color;
    }

    .user-text-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color-deep));

        box-shadow: 0px 0px 2px 1px rgba(0, 0, 0, 35%);
        border-radius: 50%;

        width: 1rem;
        height: 1rem;
    }

    .user-name {

    }
</style>
