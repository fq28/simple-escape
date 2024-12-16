import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
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
