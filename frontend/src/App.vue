<script setup>
	const bgColor = "#37353E"

</script>

<template>
	<div id="app" :style="{ backgroundColor: bgColor, margin: 0 }">
		<div class="middle-container">
			<div class="heading nunito-600">mini messenger</div>
			<div class="desc nunito-300">private and safe place to chat with your friends</div>
			<div class="input-container nunito-300">
				<input class="input-text" placeholder="your username"></input>
				<input class="input-text" placeholder="your password"></input>
			</div>
		</div>
	</div>
</template>

<style>
	@import url(./css/colors.css);
	@import url(./css/fonts.css);

	html{
		font-size: 24px;
	}

	html::selection{
		color: var(--primary-color);
		background-color: var(--accent-color);
	}

	body {
		margin: 0;
		padding: 0;
		background-color: var(--background-color);
		margin: 1rem 2rem;
	}

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

		gap: 0.5rem;
		margin: 1rem 24rem;
	}

	.input-text {
		outline: none;
		border: solid  transparent;

		font-size: 0.8rem;

		background-color: var(--deep-color);
		border-radius: 0.5rem;
		padding: 0.25rem 1rem;
		height: 2rem;
		
		color: var(--primary-color);
		caret-color: var(--accent-color);

		text-align: left;
		justify-content: center;
		width: 100%;
	}

	.input-text:hover {
		border: solid 0.125rem var(--accent-color);

		transition: border 0.3s ease-in;
	}
</style>
