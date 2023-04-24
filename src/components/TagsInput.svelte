<script lang="ts">
	import { Badge, Helper, Input, Label } from 'flowbite-svelte';
	import { newFilters } from './filterStore';

	let input = '';

	const handleCommaInput = (e: any) => {
		if (e.data == ',') {
			const value = input.split(',')[0];
			$newFilters.tags = [...new Set([...$newFilters.tags, value.trim()])];
			input = '';
		}
	};
</script>

<div class="">
	<div class="">
		<Label class="mb-2">Exclude</Label>
		<Input on:input={handleCommaInput} bind:value={input} />
		<Helper class="text-sm"
			>Enter items, separated by a list of commas, you filter away from the job title.</Helper
		>
	</div>
	{#each $newFilters.tags as tag (tag)}
		{#if tag != ''}
			<Badge
				dismissable
				on:dismiss={() => {
					$newFilters.tags = $newFilters.tags.filter((item) => item != tag);
				}}
				style="margin: 0px 3px 3px 0px"
				large>{tag}</Badge
			>
		{/if}
	{/each}
</div>
