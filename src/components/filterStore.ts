import { writable } from 'svelte/store';

interface FilterProps {
	excludeTags: string[];
	includeTags: string[];
	companies: string[];
}

export const newFilters = writable<FilterProps>({
	excludeTags: [],
	includeTags: [],
	companies: []
});

export const activeFilters = writable<FilterProps>({
	excludeTags: [],
	includeTags: [],
	companies: []
});
