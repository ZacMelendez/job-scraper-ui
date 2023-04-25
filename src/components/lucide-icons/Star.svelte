<script lang="ts">
	export let size = 24;
	export let fill = 'none';
	export let color = 'currentColor';
	let clazz: string | undefined | null;
	export { clazz as class };
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	width={size}
	height={size}
	viewBox="0 0 24 24"
	{fill}
	stroke={color}
	stroke-width="2"
	stroke-linecap="round"
	stroke-linejoin="round"
	class={`lucide lucide-star ${clazz}`}
	><polygon
		points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
	/></svg
>
