import { writable } from 'svelte/store';

export const formProps = writable({
	must: '',
	include: '',
	exclude: '',
	locations: ''
});
