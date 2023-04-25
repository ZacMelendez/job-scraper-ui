<script lang="ts">
	// @ts-nocheck
	import { Drawer, Button, CloseButton, Checkbox, Label, Helper } from 'flowbite-svelte';
	import { sineIn } from 'svelte/easing';
	import { drawerState, jobList } from '../routes/store';
	import TagsInput from './TagsInput.svelte';
	import { SlidersHorizontal } from '../components/lucide-icons';
	import { activeFilters, newFilters } from './filterStore';
	import { JobFetch, toTitleCase } from '../helpers';
	import { cloneDeep } from 'lodash';

	let disableApply: boolean;
	let disableClear: boolean;

	$: {
		disableApply =
			$activeFilters.excludeTags.toString() === $newFilters.excludeTags.toString() &&
			$activeFilters.includeTags.toString() === $newFilters.includeTags.toString() &&
			$activeFilters.companies.toString() === $newFilters.companies.toString();
	}

	$: {
		disableClear =
			!$activeFilters.excludeTags.length &&
			!$activeFilters.includeTags.length &&
			!$activeFilters.companies.length;
	}

	let transitionParams = {
		x: -320,
		duration: 200,
		easing: sineIn
	};

	const handleSearch = async () => {
		const response = await JobFetch({
			exclude: $activeFilters.excludeTags,
			include: $activeFilters.includeTags,
			companies: $activeFilters.companies
		});
		$jobList.jobs = response?.data;
		$jobList.filteredJobs = response?.data;

		$jobList.returnedJobCount = response?.data.length;
	};

	const applyFilters = () => {
		$activeFilters = cloneDeep($newFilters);
		handleSearch();
		$drawerState.hidden = true;
	};

	const handleClear = () => {
		$activeFilters = {
			excludeTags: [],
			includeTags: [],
			companies: []
		};
		$newFilters = {
			excludeTags: [],
			includeTags: [],
			companies: []
		};
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
	<div class="flex flex-row w-full justify-between mb-3">
		<Button on:click={handleClear} disabled={disableClear} color="light">Clear</Button>
		<Button on:click={applyFilters} disabled={disableApply} color="light">Apply</Button>
	</div>
	<TagsInput />
	<Label class="mt-5 mb-2">Companies</Label>
	<Helper class="text-sm mb-2"
		>Select which companies you would like to search for jobs from.</Helper
	>
	{#each ['rivian', 'american express', 'paramount', 'capital one', 'bank of america'] as company (company)}
		<Checkbox bind:group={$newFilters.companies} value={company}>
			{toTitleCase(company)}
		</Checkbox>
	{/each}
</Drawer>
