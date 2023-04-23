import { writable } from 'svelte/store';

export const newFilters = writable<{ tags: string[] }>({
	tags: []
});

export const activeFilters = writable<{ tags: string[] }>({
	tags: []
});
