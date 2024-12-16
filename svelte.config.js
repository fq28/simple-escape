import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({
			fallback: 'index.html' // For SPA routing
		}),
		paths: {
			base: '/simple-escape' // Explicitly set to match your repo name
		}
	}
};

export default config;
