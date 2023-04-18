import { writable, type Writable } from 'svelte/store';
import type { JobItemProps } from '../types';

export const jobList = writable<{
	jobs: JobItemProps[];
	filteredJobs: JobItemProps[];
	jobSearch: string;
}>({
	jobs: [],
	filteredJobs: [],
	jobSearch: ''
});

export const userStore = writable<{ userId: string; favorites: string[] }>({
	favorites: [],
	userId: ''
});

export const modalState = writable({
	opened: false
});
