<script lang="ts">
	import { Badge, Helper, Input, Label } from 'flowbite-svelte';

	let input = '';
	let tags: string[] = [];

	const handleCommaInput = (e: any) => {
		if (e.data == ',') {
			const value = input.split(',')[0];
			tags = [...new Set([...tags, value.trim()])];
			input = '';
		}
	};
</script>

<div class="grid grid-cols-2 gap-4">
	<div class="col-span-2">
		<Label class="mb-2">Exclude</Label>
		<Input bind:value={input} on:input={handleCommaInput} />
		<Helper class="text-sm"
			>Enter items, separated by a list of commas, you filter away from the job title.</Helper
		>
	</div>
	{#each tags as tag}
		{#if tag != ''}
			<Badge
				dismissable
				on:dismiss={(e) => {
					tags = tags.filter((item) => item != tag);
				}}
				large>{tag}</Badge
			>
		{/if}
	{/each}
</div>
