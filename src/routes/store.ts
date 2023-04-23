import { writable } from 'svelte/store';
import type { JobItemProps } from '../types';

export const jobList = writable<{
	jobs: JobItemProps[];
	filteredJobs: JobItemProps[];
	jobSearch: string;
	returnedJobCount: number;
	searched: boolean;
}>({
	jobs: [],
	filteredJobs: [],
	jobSearch: '',
	returnedJobCount: 20,
	searched: false
});

export const userStore = writable<{ userId: string; favorites: string[] }>({
	favorites: [],
	userId: ''
});

export const drawerState = writable({
	hidden: true
});
