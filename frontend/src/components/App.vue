<template>
    <div id="app">
        <router-view></router-view>
    </div>
</template>

<script>
    export default {
        name: "App",
    }
</script>

<style>
	#app {
		height: 100vh;
		align-content: center;
	}
	html{
		font-size: 24px;
    	font-size: clamp(20px, 2vw, 24px);
		overflow: hidden;
	}

	html::selection{
		color: var(--white-color);
		background-color: var(--primary-color);
	}

	body {
		margin: 0;
		padding: 0;
		background-color: var(--background-color);
		/* margin: 1rem 2rem; */
	}

	img {
		user-select: none;
	}
</style>
