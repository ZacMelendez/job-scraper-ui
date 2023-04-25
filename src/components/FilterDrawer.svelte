<script lang="ts">
	// @ts-nocheck
	import { Drawer, Button, CloseButton, Checkbox, Label, Helper } from 'flowbite-svelte';
	import { sineIn } from 'svelte/easing';
	import { drawerState, jobList } from '../routes/store';
	import TagsInput from './TagsInput.svelte';
	import { SlidersHorizontal } from 'lucide-svelte';
	import { activeFilters, newFilters } from './filterStore';
	import { JobFetch, toTitleCase } from '../helpers';

	let enableApply: boolean;

	$: {
		enableApply =
			$activeFilters.excludeTags.toString() == $newFilters.excludeTags.toString() &&
			$activeFilters.includeTags.toString() == $newFilters.includeTags.toString() &&
			$activeFilters.companies.toString() == $newFilters.companies.toString();
	}

	$: {
		$newFilters.companies = Object.entries(companies)
			.filter((item) => item[1])
			.map((item) => {
				return item[0];
			});
	}

	const companies = {
		'american express': false,
		'capital one': false,
		'bank of america': false,
		paramount: false
	};

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
		$activeFilters = $newFilters;
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
	<Label class="mt-5 mb-2">Companies</Label>
	<Helper class="text-sm">Select which companies you would like to search for jobs from.</Helper>
	{#each Object.keys(companies) as company}
		<Checkbox
			on:click={() => {
				companies[company] = !companies[company];
			}}
			value={companies[company]}
		>
			{toTitleCase(company)}
		</Checkbox>
	{/each}
</Drawer>
