<template>
    <div class="new-chat-popup" id="new-chat">
        <div class="create-form input-container">
			<form id="authorization-form" v-on:submit="createNewChat">
                <div class="header">
                    <div class="form-heading nunito-600" style="width: 100%;">Create Chat</div>
                    <div class="mini-button" v-on:click="flipContent('new-chat')"><font-awesome-icon icon="arrow-right" style="display: block; width: 0.75rem; height: 0.75rem;"></font-awesome-icon></div>
                </div>
				<label class="error nunito-400" id="error-msg"></label>
				<label class="approve nunito-400" id="approve-msg"></label>
				<input class="input-text" type="text" placeholder="your chat name" required v-model="chatName"></input>
				<select class="input-text" id="chat-select" v-model="chatType">
                    <option value="Public">
                        ✨ Public
                    </option>
                    <option value="Private">
                        🔒 Private
                    </option>
                </select>
				<input class="input-text" type="email" placeholder="add member..." v-model="invitedUserEmail"></input>
				<div class="button-container">
					<input type="submit" value="Create New Chat" class="button-1 nunito-600"></input>
				</div>
			</form>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                chatName: "",
                chatType: "",
                invitedUserEmail: "",
            }
        },

        methods: {
            async createNewChat(event) {
                event.preventDefault();
                console.log(this.chatType);
                console.log(this.chatName);
                console.log(this.invitedUserEmail);

                const invitedUserResponse = await fetch(`/api/users?email=${this.invitedUserEmail}`);
                const response = await fetch(`/api/users/me/chats?invited_user_id=${new Number((await invitedUserResponse.json()).id)}&name=${this.chatName}&type=${this.chatType}`, {
                    method: "POST"
                });

                console.log(await response.json());
            },
        }
    }
</script>


<script setup>
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
        background-color: rgba(0, 0, 0, 0.1);
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
