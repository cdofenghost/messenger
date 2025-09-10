<template>
	<div class="middle-container">
		<div class="heading nunito-600">mini messenger</div>
		<div class="desc nunito-300">private and safe place to chat with your friends</div>
		<div class="input-container nunito-300">
			<input class="input-text" placeholder="your username"></input>
			<input class="input-text" type="password" placeholder="your password"></input>
		</div>
		<div class="button-container">
			<router-link style="width: 100%;" to="/funchat">
				<button class="button-1 nunito-600">Sign In</button>
			</router-link>
			<router-link style="width: 100%;" to="/register">
				<button class="button-1 nunito-600">Sign Up</button>
			</router-link>
		</div>
	</div>
</template>

<script>
</script>

<style scoped>
	@import url(../css/colors.css);
	@import url(../css/fonts.css);

	.heading {
		text-align: center;
		font-size: 2rem;
		color: var(--primary-color);
	}

	.desc {
		text-align: center;
		font-size: 1rem;
		color: var(--primary-color);
	}

	.middle-container {
		border: 4px solid var(--accent-color);
		border-radius: 1rem;
		box-sizing: content-box;
		align-content: center;

		height: 94vh;
	}

	.input-container {
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
		margin-top: 1rem;

		width: 24rem;
		gap: 0.5rem;
	}

	.button-1 {
		border: none;
		height: 1.5rem;
		width: 100%;

		border-radius: 0.25rem;
		background-color: var(--accent-color);
		color: var(--primary-color);

		transition:
			background-color 0.1s ease-out,
			color 0.1s ease-out;
	}

	.button-1:hover {
		background-color: var(--primary-color);
		color: var(--accent-color);

		transition:
			background-color 0.1s ease-in,
			color 0.1s ease-in;
	}

	.input-text {
		outline: none;
		border: solid 0.125rem transparent;
		box-sizing: border-box;

		font-size: 0.8rem;

		background-color: var(--deep-color);
		border-radius: 0.5rem;
		padding: 0.25rem 1rem;
		height: 2rem;
		
		color: var(--primary-color);
		caret-color: var(--accent-color);

		width: 100%;

		text-align: left;
		justify-content: center;

		transition:
			border 0.1s ease-out;
	}

	.input-text:hover {
		border: solid 0.125rem var(--accent-color);
		transition: border 0.3s ease-in;
	}
</style>
