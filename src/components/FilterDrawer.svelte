<script lang="ts">
	import { Drawer, Button, CloseButton } from 'flowbite-svelte';
	import { sineIn } from 'svelte/easing';
	import { drawerState, jobList } from '../routes/store';
	import TagsInput from './TagsInput.svelte';
	import { SlidersHorizontal } from 'lucide-svelte';
	import { activeFilters, newFilters } from './filterStore';
	import { JobFetch } from '../helpers';

	let enableApply: boolean;

	$: enableApply = $activeFilters.tags.toString() == $newFilters.tags.toString();

	let transitionParams = {
		x: -320,
		duration: 200,
		easing: sineIn
	};

	const handleSearch = async () => {
		const response = await JobFetch({ search: $jobList.jobSearch, exclude: $activeFilters.tags });
		$jobList.jobs = response?.data;
		$jobList.filteredJobs = response?.data;

		$jobList.returnedJobCount = response?.data.length;
	};

	const applyFilters = () => {
		$activeFilters.tags = $newFilters.tags;
		handleSearch();
	};
</script>

<Drawer
	class="flex flex-col"
	transitionType="fly"
	{transitionParams}
	bind:hidden={$drawerState.hidden}
	id="sidebar1"
>
	<div class="flex items-center">
		<h5
			id="drawer-label"
			class="inline-flex items-center mb-4 text-base font-semibold text-gray-500 dark:text-gray-400"
		>
			<SlidersHorizontal size={16} style="margin-right: 10px" />Filters
		</h5>
		<CloseButton on:click={() => ($drawerState.hidden = true)} class="mb-4 dark:text-white" />
	</div>
	<Button on:click={applyFilters} disabled={enableApply} style="align-self: flex-end" color="light"
		>Apply</Button
	>
	<TagsInput />
</Drawer>
