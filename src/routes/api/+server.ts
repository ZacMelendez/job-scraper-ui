import { marshall } from '@aws-sdk/util-dynamodb';
import { queryTable } from '../../helpers/JobsDatabase';
import { updateFavorites } from '../../helpers/UserDatabase';

import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	const { user_id, favorites } = await request.json();

	await updateFavorites({ user_id, favorites });

	return json({ status: 'success' }, { status: 201 });
}

export async function GET({ url }) {
	const search = url.searchParams.get('search')?.toLowerCase() ?? undefined;
	const exclude = url.searchParams.get('exclude')?.toLowerCase() ?? undefined;
	const lastEvalKey = url.searchParams.get('lastEvalKey')?.toLowerCase() ?? undefined;

	const excludeList = exclude?.split(',');

	console.log({ lastEvalKey, search, exclude });

	// const data = await getJobs({ lastEvalKey, search });

	const data = await queryTable({
		search: search,
		exclusiveStartKey: lastEvalKey ? marshall({ type: 'job', jobUrl: lastEvalKey }) : undefined,
		excludeList
	});

	return json({ data: data }, { status: 201 });
}
