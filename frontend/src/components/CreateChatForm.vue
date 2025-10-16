<template>
    <div class="new-chat-popup" id="new-chat">
        <div class="create-form input-container">
			<form id="authorization-form" v-on:submit="createNewChat">
                <div class="header">
                    <div class="form-heading nunito-600" style="width: 100%;">Create Chat</div>
                    <div class="mini-button" v-on:click="flipContent('new-chat')"><font-awesome-icon icon="arrow-right" style="display: block; width: 0.75rem; height: 0.75rem;"></font-awesome-icon></div>
                </div>
				<ErrorPopup></ErrorPopup>
				<ApprovePopup></ApprovePopup>
				<input class="input-text" type="text" placeholder="your chat name" required v-model="chatName"></input>
				<select class="input-text" id="chat-select" v-model="chatType">
                    <option value="Public">
                        ✨ Public
                    </option>
                    <option value="Private">
                        🔒 Private
                    </option>
                </select>
				<input v-on:input="debouncedSearch" class="input-text" placeholder="add member..." v-model="userSearch"></input>
				<div class="added-users">
					<AddedUser
						v-for="user in invitedUsers"
						@delete="handleDelete"
						:userReference="user"
						:userName="user.name"
						:userIcon=null>
					</AddedUser>
				</div>
				<div class="search-results">
					<UserSearchResult 
						v-for="user in usersInSearch"
						@update:invitedUsers="handleInvitationUpdate"
						:userReference="user"
						:invitedUsers="invitedUsers"
						:userId="user.id"
						:userName="user.name"
						:userTag="user.tag"
						:userIcon="null">
					</UserSearchResult>
				</div>
				<div class="button-container">
					<input type="submit" value="Create New Chat" class="button-1 nunito-600"></input>
				</div>
			</form>
        </div>
    </div>
</template>

<script setup>
	import { computed, ref } from 'vue';
	import UserSearchResult from './UserSearchResult.vue';
	import AddedUser from './AddedUser.vue';
	import ErrorPopup from './ErrorPopup.vue';
	import ApprovePopup from './ApprovePopup.vue';

	const chatName = ref("");
	const chatType = ref("Public");
	const userSearch = ref("");
	const invitedUsers = ref([]);
	const invitedUserIds = ref([]);
	const usersInSearch = ref(null);

	let timerReference = null;

	async function createNewChat(event) {
		event.preventDefault();
		// console.log(this.chatType);
		// console.log(this.chatName);
		// console.log(this.userSearch);
		const response = await fetch(`/api/users/me/chats?name=${chatName.value}&type=${chatType.value}`, {
			headers: {
				"Content-Type": "application/json",	
			},
			method: "POST",
			body: JSON.stringify(invitedUserIds.value),
		});

		console.log(await response.json());
	}

	function handleDelete(userToDelete)
	{
		invitedUsers.value = invitedUsers.value.filter(user => user != userToDelete)
		invitedUserIds.value = [];
		invitedUsers.value.forEach(user => {
			invitedUserIds.value.push(user.id);
		});
		console.log(userToDelete);
	}

	function handleInvitationUpdate(newValue)
	{
		invitedUsers.value.push(newValue);
		invitedUserIds.value.push(newValue.id);
		console.log(invitedUserIds.value);
	}

	async function debouncedSearch(params) 
	{
		if (timerReference == null)
		{
			timerReference = setTimeout(async () => searchForUser(), 1000);
		}
		else
		{
			timerReference = clearTimeout(timerReference);
			timerReference = setTimeout(async () => searchForUser(), 1000);
		}
	}

	async function searchForUser()
	{
		try {
			const invitedUserResponse = await fetch(`/api/users/search?query=${userSearch.value}`);
			if (invitedUserResponse.ok)
			{
				usersInSearch.value = await invitedUserResponse.json();
				console.log(usersInSearch.value);
			}
			else 
			{
				usersInSearch.value = [];
			}

		} catch (error) {
			console.error(error);
		}
	}

    function flipContent(switchType)
    {
        const hiddenContent = document.getElementById(switchType); 

        if (hiddenContent.classList.contains('show')) hiddenContent.classList.remove('show');
        else hiddenContent.classList.add('show');
    }
</script>
<style scoped>
    @import url("../css/fonts.css");
    @import url("../css/colors.css");

	.added-users {
        display: flex;
		justify-content: start;
		width: 100%;
		gap: 0.25rem;
	}

	.search-results {
		display: flex;
		flex-direction: column;
		flex-grow: 1;
		gap: 0.25rem;

		padding-left: 1rem;
		box-sizing: border-box;
		width: 100%;
	}
    .header {
        display: flex; 
        justify-items: space-between; 
        align-items: center;

        width: 100%; 
        padding: 0.5rem; 
        box-sizing: border-box;
    }
    .form-heading {
        text-align: center;
    }

    .mini-button {
        padding: 0.25rem;
        border-radius: 50%;

        transition: 0.2s ease-out background-color;
    }
    
    .mini-button:hover {
        background-color: var(--grey-color);

        transition: 0.1s ease-in background-color;
    }

    .new-chat-popup {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 10%);
        display: none;
        z-index: 9999;
        justify-items: center;
        align-content: center;

		opacity: 0;
        transition: 0.3s ease-out opacity;
    }

    .create-form {
		background-color: var(--background-color);
		border-radius: 1rem;
		box-sizing: content-box;
		height: fit-content;

        padding: 1rem;
    }


	.input-container form {
		display: flex;
		flex-direction: column;
		box-sizing: border-box;

		align-items: center;
		justify-self: center;

		margin-top: 1rem;

		width: 24rem;
		gap: 0.5rem;
	}

	.button-container {
		display: flex;
		box-sizing: border-box;

		justify-content: center;
		justify-self: center;

		width: 24rem;
		gap: 0.5rem;
	}

	.button-1 {
		border: none;
		height: 1.5rem;
		width: 100%;

		border-radius: 0.25rem;
		background-color: var(--primary-color);
		color: var(--white-color);

		transition:
			background-color 0.1s ease-out,
			color 0.1s ease-out;
	}

	.button-1:hover {
		background-color: var(--accent-color-deep);

		transition:
			background-color 0.1s ease-in,
			color 0.1s ease-in;
	}

	.input-text {
		outline: none;
		border: solid 0.125rem transparent;
		box-sizing: border-box;

		font-size: 0.8rem;

		background-color: var(--grey-color);
		border-radius: 0.5rem;
		padding: 0.25rem 1rem;
		height: 2rem;
		
		color: var(--primary-color-contrast);
		caret-color: var(--accent-color-deep);

		width: 100%;

		text-align: left;
		justify-content: center;

		transition:
			border 0.1s ease-out;
	}

	.error, .approve {
		color: white;
		background-color: var(--error-color);
		height: fit-content;

		border-radius: .25rem;
		font-style: italic;
		font-size: medium;

		opacity: 0;
		display: none;

		transform: translateY(-10px), scale(0);
		padding: 0.5em 1em;
		position: relative;
		z-index: 1000;

		transition: all 0.3s ease;
		transition-property: overlay display opacity transform;
		transition-duration: 0.3s;
		transition-behavior: allow-discrete;
	}

	.error.show, .approve.show {
		display: block;

		opacity: 1;
		transform: translateY(0), scale(1);
		@starting-style {
			opacity: 0;
		}
	}

	.approve {
		background-color: var(--success-color);
	}

	.input-text:hover {
		border: solid 0.125rem var(--primary-color);
		transition: border 0.3s ease-in;
	}
</style>
