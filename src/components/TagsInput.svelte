<script lang="ts">
	import { Badge, Helper, Input, Label } from 'flowbite-svelte';
	import { newFilters } from './filterStore';

	let excludeInput = '';
	let includeInput = '';
</script>

<div class="">
	<div class="">
		<Label class="mb-2">Exclude</Label>
		<Input
			on:input={(e) => {
				// @ts-ignore
				if (e.data === ',') {
					const value = excludeInput.split(',')[0];
					$newFilters.excludeTags = [...new Set([...$newFilters.excludeTags, value.trim()])];
					excludeInput = '';
				}
			}}
			bind:value={excludeInput}
		/>
		<Helper class="text-sm"
			>Enter items, separated by a list of commas, you would like to filter away from the job title.</Helper
		>
	</div>
	{#each $newFilters.excludeTags as tag (tag)}
		{#if tag != ''}
			<Badge
				dismissable
				on:dismiss={() => {
					$newFilters.excludeTags = $newFilters.excludeTags.filter((item) => item != tag);
				}}
				style="margin: 0px 3px 3px 0px"
				large>{tag}</Badge
			>
		{/if}
	{/each}
	<div class="">
		<Label class="mt-5 mb-2">Include</Label>
		<Input
			on:input={(e) => {
				// @ts-ignore
				if (e.data === ',') {
					const value = includeInput.split(',')[0];
					$newFilters.includeTags = [...new Set([...$newFilters.includeTags, value.trim()])];
					includeInput = '';
				}
			}}
			bind:value={includeInput}
		/>
		<Helper class="text-sm"
			>Enter items, separated by a list of commas, you would like to include in the job title.</Helper
		>
	</div>
	{#each $newFilters.includeTags as tag (tag)}
		{#if tag != ''}
			<Badge
				dismissable
				on:dismiss={() => {
					$newFilters.includeTags = $newFilters.includeTags.filter((item) => item != tag);
				}}
				style="margin: 0px 3px 3px 0px"
				large>{tag}</Badge
			>
		{/if}
	{/each}
</div>
