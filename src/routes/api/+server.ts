import { getJobs } from '../../helpers/JobsDatabase';
import { updateFavorites } from '../../helpers/UserDatabase';

import { json } from '@sveltejs/kit';

export async function POST({ request }) {
	const { user_id, favorites } = await request.json();

	await updateFavorites({ user_id, favorites });

	return json({ status: 'success' }, { status: 201 });
}

export async function GET({ url }) {
	const lastEvalKey = url.searchParams.get('lastEvalKey')?.toLowerCase() ?? undefined;
	const search = url.searchParams.get('search')?.toLowerCase() ?? undefined;

	const data = await getJobs({ lastEvalKey, search });

	return json({ data: data }, { status: 201 });
}
