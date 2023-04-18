<div>
	<ul>
		{#each [...new Array(10)] as item}
			<li class="loading-item">
				<div class="skeleton-card-text" style="display: flex;flex-direction: row">
					<div style="width: 40%">
						<div class="skeleton skeleton-card-title" />
						<div class="skeleton skeleton-card-brand" />
						<div class="skeleton skeleton-card-brand" />
					</div>
				</div>
			</li>
		{/each}
	</ul>
</div>

<style lang="scss">
	.loading-item {
		background: #e7ebea;
		padding: 0 30px;
	}
	.skeleton {
		border-radius: 0.25rem;
		animation: skeleton-loading 1s linear infinite alternate;
	}

	.skeleton-card-brand {
		width: 70%;
		height: 0.7rem;
		margin: 0.5rem;
		border-radius: 0.25rem;
	}

	.skeleton-card-text {
		padding: 10px;
	}

	.skeleton-card-title {
		width: 100%;
		height: 0.9rem;
		margin: 0.5rem;
	}

	@keyframes skeleton-loading {
		0% {
			background-color: var(--skeleton-loader-dark);
		}
		100% {
			background-color: var(--skeleton-loader-light);
		}
	}
</style>
