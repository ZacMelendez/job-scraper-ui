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
	const include = url.searchParams.get('include')?.toLowerCase() ?? undefined;
	const exclude = url.searchParams.get('exclude')?.toLowerCase() ?? undefined;
	const companies = url.searchParams.get('companies')?.toLowerCase() ?? undefined;
	const lastEvalKey = url.searchParams.get('lastEvalKey')?.toLowerCase() ?? undefined;

	const excludeList = exclude?.split(',');
	const includeList = include?.split(',');
	const companyList = companies?.split(',');

	const data = await queryTable({
		includeList,
		exclusiveStartKey: lastEvalKey ? marshall({ type: 'job', jobUrl: lastEvalKey }) : undefined,
		excludeList,
		companyList
	});

	return json({ data: data }, { status: 201 });
}
