<template>
    <div class="members">
        <MemberCard
        v-for="user in members"
        :userName="user.name"
        :userIcon="null"
        :userId="user.id"
        :userTag="user.tag"></MemberCard>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import MemberCard from './MemberCard.vue';

const props = defineProps({
    chatId: {
        type: Number,
        default: null,
    }
});

const members = ref(null);
const response = await fetch(`/api/chats/${props.chatId}/members`);
console.log(props.chatId)
members.value = await response.json();
console.log(members.value);

</script>

<style>
    .members {
        width: 12rem;
    }
</style>
