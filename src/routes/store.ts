import { writable, type Writable } from 'svelte/store';
import type { JobItemProps } from '../types';

export const jobList = writable<{ jobs: JobItemProps[] }>({
	jobs: []
});
