<script>
	import { Drawer, Button, CloseButton } from 'flowbite-svelte';
	import { sineIn } from 'svelte/easing';
	import { drawerState } from '../routes/store';
	import TagsInput from './TagsInput.svelte';
	import { SlidersHorizontal } from 'lucide-svelte';

	let transitionParams = {
		x: -320,
		duration: 200,
		easing: sineIn
	};
</script>

<Drawer transitionType="fly" {transitionParams} bind:hidden={$drawerState.hidden} id="sidebar1">
	<div class="flex items-center">
		<h5
			id="drawer-label"
			class="inline-flex items-center mb-4 text-base font-semibold text-gray-500 dark:text-gray-400"
		>
			<SlidersHorizontal size={16} style="margin-right: 10px" />Filters
		</h5>
		<CloseButton on:click={() => ($drawerState.hidden = true)} class="mb-4 dark:text-white" />
	</div>
	<TagsInput />
</Drawer>
